"""
Author: Martin Craig <martin.craig@eng.ox.ac.uk>
Copyright (c) 2016-2017 University of Oxford, Martin Craig
"""

from __future__ import division, unicode_literals, absolute_import, print_function

import sys
import os
import time
import traceback
import re
import tempfile

try:
    from PySide import QtGui, QtCore, QtGui as QtWidgets
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets

from quantiphyse.gui.widgets import QpWidget, HelpButton, BatchButton, OverlayCombo, RoiCombo, NumericOption, NumberList, LoadNumbers, OrderList, OrderListButtons, Citation, TitleWidget, RunBox
from quantiphyse.gui.dialogs import TextViewerDialog, error_dialog, GridEditDialog
from quantiphyse.processes import Process
from quantiphyse.utils import get_plugins, QpException

CEST_CITE_TITLE = "Quantitative Bayesian model-based analysis of amide proton transfer MRI"
CEST_CITE_AUTHOR = "Chappell, M. A., Donahue, M. J., Tee, Y. K., Khrapitchev, A. A., Sibson, N. R., Jezzard, P., & Payne, S. J."
CEST_CITE_JOURNAL = "Magnetic Resonance in Medicine. doi:10.1002/mrm.24474"

B0_DEFAULTS = ["3T", "9.4T", "Custom"]

# Gyromagnetic ratio / 2PI
GYROM_RATIO_BAR = 42.5774806e6

from ._version import __version__

class Pool:
    def __init__(self, name, enabled, vals=None, userdef=False):
        self.name = name
        self.enabled = enabled
        if vals is None: vals = {}
        for b0 in B0_DEFAULTS:
            if b0 not in vals: vals[b0] = [0, 0, 0, 0]
        self.original_vals = vals
        self.userdef = userdef
        self.reset()

    def reset(self):
        self.vals = dict(self.original_vals)

class NewPoolDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(NewPoolDialog, self).__init__(parent)
        self.setWindowTitle("New Pool")
        vbox = QtGui.QVBoxLayout()

        grid = QtGui.QGridLayout()

        grid.addWidget(QtGui.QLabel("Name"), 0, 0)
        self.name_edit = QtGui.QLineEdit()
        self.name_edit.editingFinished.connect(self._validate)
        grid.addWidget(self.name_edit, 0, 1, 1, 3)
        
        self.ppm = NumericOption("PPM", grid, ypos=1, xpos=0, default=0, spin=False)
        self.ppm.sig_changed.connect(self._validate)
        self.exc = NumericOption("Exchange rate", grid, ypos=2, xpos=0, default=0, spin=False)
        self.exc.sig_changed.connect(self._validate)
        self.t1 = NumericOption("T1", grid, ypos=1, xpos=2, default=1.0, spin=False)
        self.t1.sig_changed.connect(self._validate)
        self.t2 = NumericOption("T2", grid, ypos=2, xpos=2, default=1.0, spin=False)
        self.t2.sig_changed.connect(self._validate)

        vbox.addLayout(grid)

        self.button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        vbox.addWidget(self.button_box)

        self.setLayout(vbox)
        self._validate()
    
    def pool(self, b0):
        return Pool(self.name_edit.text(), True, 
                    vals={b0 : [w.value() for w in [self.ppm, self.exc, self.t1, self.t2]]},
                    userdef=True)

    def _validate(self):
        valid = self.ppm.valid and self.exc.valid and self.t1.valid and self.t2.valid
        
        if self.name_edit.text() != "":
            self.name_edit.setStyleSheet("")
        else:
            self.name_edit.setStyleSheet("QLineEdit {background-color: red}")
            valid = False
        
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(valid)

class CESTWidget(QpWidget):
    """
    CEST-specific widget, using the Fabber process
    """

    pools = [
        Pool("Water", True, {"3T" : [0, 0, 1.3, 0.07], "9.4T" : [0, 0, 1.9, 0.07]}),
        Pool("Amide", True, {"3T" : [3.5, 20, 0.77, 0.01], "9.4T" : [3.5, 20, 1.1, 0.01]}),
        Pool("NOE/MT", True, {"3T" : [-2.41, 30, 1.0, 0.0002], "9.4T" : [-2.41, 30, 1.5, 0.0002]}),
        Pool("NOE", False, {"3T" : [-3.5, 20, 0.77, 0.0003], "9.4T" : [-3.5, 20, 1.1, 0.0003]}),
        Pool("MT", False, {"3T" : [0, 60, 1.0, 0.0001], "9.4T" : [0, 60, 1.5, 0.0001]}),
        Pool("Amine", False, {"3T" : [2.8, 500, 1.23, 0.00025], "9.4T" : [2.8, 500, 1.8, 0.00025]}),
    ]

    def __init__(self, **kwargs):
        QpWidget.__init__(self, name="QuantiCEST", icon="cest", group="CEST", desc="Bayesian CEST analysis", **kwargs)
        
    def init_ui(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        try:
            self.fabber_process = get_plugins("processes", "FabberProcess")[0]
        except:
            self.fabber_process = None

        if self.fabber_process is None:
            vbox.addWidget(QtGui.QLabel("Fabber core library not found.\n\n You must install Fabber to use this widget"))
            return
    
        title = TitleWidget(self, help="cest", subtitle="Bayesian Modelling for Chemical Exchange Saturation Transfer MRI %s" % __version__)
        vbox.addWidget(title)
        
        cite = Citation(CEST_CITE_TITLE, CEST_CITE_AUTHOR, CEST_CITE_JOURNAL)
        vbox.addWidget(cite)

        seq_box = QtGui.QGroupBox()
        seq_box.setTitle("Sequence")
        grid = QtGui.QGridLayout()
        grid.setColumnStretch(4, 1)
        seq_box.setLayout(grid)

        # Table of frequency offsets
        grid.addWidget(QtGui.QLabel("Frequency offsets"), 0, 0)
        self.freq_offsets = NumberList([1, 2, 3, 4, 5])
        grid.addWidget(self.freq_offsets, 0, 1, 1, 4)
        self.load_freq_offsets = LoadNumbers(self.freq_offsets)
        grid.addWidget(self.load_freq_offsets, 0, 5)

        self.data_combo = OverlayCombo(self.ivm)
        grid.addWidget(QtGui.QLabel("CEST data"), 1, 0)
        grid.addWidget(self.data_combo, 1, 1)
        self.roi_combo = RoiCombo(self.ivm)
        grid.addWidget(QtGui.QLabel("ROI"), 1, 2)
        grid.addWidget(self.roi_combo, 1, 3)
        
        # Field strength - this affects pool values selected
        grid.addWidget(QtGui.QLabel("B0"), 2, 0)
        self.b0_combo = QtGui.QComboBox()
        self.poolval_combo = QtGui.QComboBox()
        for b0 in B0_DEFAULTS:
            self.b0_combo.addItem(b0)
        self.b0_combo.currentIndexChanged.connect(self.b0_changed)
        grid.addWidget(self.b0_combo, 2, 1)

        self.b0_custom = QtGui.QWidget()
        hbox = QtGui.QHBoxLayout()
        self.b0_custom.setLayout(hbox)
        self.b0_spin = QtGui.QDoubleSpinBox()
        self.b0_spin.setValue(3.0)
        self.b0_spin.valueChanged.connect(self.b0_changed)
        hbox.addWidget(self.b0_spin)
        hbox.addWidget(QtGui.QLabel("T"))
        label = QtGui.QLabel("WARNING: Pool values will need editing")
        label.setStyleSheet("QLabel { color : red; }")
        hbox.addWidget(label)
        grid.addWidget(self.b0_custom, 2, 2, 1, 4)

        # B1 field
        self.b1 = NumericOption("B1 (\u03bcT)", grid, ypos=3, xpos=0, default=0.55, decimals=6)
        #hbox = QtGui.QHBoxLayout()
        #self.unsat_cb = QtGui.QCheckBox("Unsaturated")
        #self.unsat_cb.stateChanged.connect(self.update_ui)
        #hbox.addWidget(self.unsat_cb)
        #self.unsat_combo = QtGui.QComboBox()
        #self.unsat_combo.addItem("first")
        #self.unsat_combo.addItem("last")
        #self.unsat_combo.addItem("first and last  ")
        #hbox.addWidget(self.unsat_combo)
        #hbox.addStretch(1)
        #grid.addLayout(hbox, 2, 2)
        
        grid.addWidget(QtGui.QLabel("Saturation"), 3, 2)
        self.sat_combo = QtGui.QComboBox()
        self.sat_combo.addItem("Continuous Saturation   ")
        self.sat_combo.addItem("Pulsed Saturation   ")
        self.sat_combo.currentIndexChanged.connect(self.update_ui)
        self.sat_combo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        grid.addWidget(self.sat_combo, 3, 3)

        # Continuous saturation
        self.st = NumericOption("Saturation times (s)", grid, ypos=4, xpos=0, default=2.0)

        # Pulsed saturation
        self.pms_label = QtGui.QLabel("Pulse Magnitudes")
        grid.addWidget(self.pms_label, 5, 0)
        self.pms = NumberList([0, 0, 0, 0])
        grid.addWidget(self.pms, 5, 1, 1, 2)
        self.load_pms = LoadNumbers(self.pms)
        grid.addWidget(self.load_pms, 5, 3)
        self.pds_label = QtGui.QLabel("Pulse Durations (s)")
        grid.addWidget(self.pds_label, 6, 0)
        self.pds = NumberList([0, 0, 0, 0])
        grid.addWidget(self.pds, 6, 1, 1, 2)
        self.load_pds = LoadNumbers(self.pds)
        grid.addWidget(self.load_pds, 6, 3)
        self.pr = NumericOption("Pulse Repeats", grid, ypos=7, xpos=0, default=1, intonly=True)
        
        vbox.addWidget(seq_box)
    
        # Pools
        pool_box = QtGui.QGroupBox()
        pool_box.setTitle("Pools")
        pool_vbox = QtGui.QVBoxLayout()
        pool_box.setLayout(pool_vbox)

        self.poolgrid = QtGui.QGridLayout()
        self.populate_poolgrid()
        pool_vbox.addLayout(self.poolgrid)

        hbox = QtGui.QHBoxLayout()
        self.custom_label = QtGui.QLabel("")
        self.custom_label.setStyleSheet("QLabel { color : red; }")
        hbox.addWidget(self.custom_label)
        new_btn = QtGui.QPushButton("New Pool")
        new_btn.clicked.connect(self.new_pool)
        hbox.addWidget(new_btn)
        edit_btn = QtGui.QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_pools)
        hbox.addWidget(edit_btn)
        reset_btn = QtGui.QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_pools)
        hbox.addWidget(reset_btn)
        pool_vbox.addLayout(hbox)
        pool_vbox.addStretch(1)

        # Fabber Options
        analysis_box = QtGui.QGroupBox()
        analysis_box.setTitle("Analysis")
        anVbox = QtGui.QVBoxLayout()
        analysis_box.setLayout(anVbox)

        grid = QtGui.QGridLayout()
        self.spatial_cb = QtGui.QCheckBox("Spatial regularization")
        grid.addWidget(self.spatial_cb, 0, 0, 1, 2)
        self.t12_cb = QtGui.QCheckBox("Allow uncertainty in T1/T2 values")
        self.t12_cb.stateChanged.connect(self.update_ui)
        grid.addWidget(self.t12_cb, 1, 0, 1, 2)
        self.t1_cb = QtGui.QCheckBox("T1 map")
        self.t1_cb.stateChanged.connect(self.update_ui)
        grid.addWidget(self.t1_cb, 2, 0)
        self.t1_ovl = OverlayCombo(self.ivm, static_only=True)
        self.t1_ovl.setEnabled(False)
        grid.addWidget(self.t1_ovl, 2, 1)
        self.t2_cb = QtGui.QCheckBox("T2 map")
        self.t2_cb.stateChanged.connect(self.update_ui)
        grid.addWidget(self.t2_cb, 3, 0)
        self.t2_ovl = OverlayCombo(self.ivm, static_only=True)
        self.t2_ovl.setEnabled(False)
        grid.addWidget(self.t2_ovl, 3, 1)
        anVbox.addLayout(grid)

        self.pvc_cb = QtGui.QCheckBox("Tissue PV map (GM+WM)")
        self.pvc_cb.stateChanged.connect(self.update_ui)
        grid.addWidget(self.pvc_cb, 4, 0)
        self.pv_ovl = OverlayCombo(self.ivm, static_only=True)
        self.pv_ovl.setEnabled(False)
        grid.addWidget(self.pv_ovl, 4, 1)
        
        # Output Options
        output_box = QtGui.QGroupBox()
        output_box.setTitle("Output")
        grid = QtGui.QGridLayout()
        output_box.setLayout(grid)

        self.output_rstar = QtGui.QCheckBox("CEST R*")
        self.output_rstar.setChecked(True)
        grid.addWidget(self.output_rstar, 0, 0)
        self.output_params = QtGui.QCheckBox("Parameter maps")
        grid.addWidget(self.output_params, 1, 0)
        #self.output_vars = QtGui.QCheckBox("Parameter variance")
        #grid.addWidget(self.output_vars, 2, 0)
        self.output_modelfit = QtGui.QCheckBox("Model fit")
        grid.addWidget(self.output_modelfit, 2, 0)
        grid.setRowStretch(3, 1)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(pool_box)
        hbox.addWidget(analysis_box)
        hbox.addWidget(output_box)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        run_tabs = QtGui.QTabWidget()
        
        run_box = RunBox(self.get_process_model, self.get_rundata_model, title="Run model-based analysis", save_option=True)
        run_tabs.addTab(run_box, "Model based analysis")
        
        run_box = RunBox(self.get_process_lda, self.get_rundata_lda, title="Run Lorentzian Difference analysis", save_option=True)
        run_tabs.addTab(run_box, "Lorentzian Difference analysis")
        
        vbox.addWidget(run_tabs)

        vbox.addStretch(1)

        self.poolvals_edited = False
        self.b0_combo.setCurrentIndex(1)
        self.update_ui()

    def populate_poolgrid(self):
        row, col = 0, 0
        NUM_POOL_COLS = 3
        for pool in self.pools:
            if col == NUM_POOL_COLS:
                col = 0
                row += 1
            existing = self.poolgrid.itemAtPosition(row, col)
            if existing is not None:
                existing.widget().setParent(None)
            cb = QtGui.QCheckBox(pool.name)
            cb.setChecked(pool.enabled)
            cb.stateChanged.connect(self.pool_enabled(pool))
            self.poolgrid.addWidget(cb, row, col)
            col += 1

    def pool_enabled(self, pool):
        def cb(state):
            pool.enabled = state
        return cb

    def b0_changed(self):
        self.b0_sel = self.b0_combo.currentText()
        if self.b0_combo.currentIndex() == 2:
            # Custom B0
            self.b0_custom.setVisible(True)
            self.b0 = self.b0_spin.value()
        else:
            self.b0_custom.setVisible(False)
            self.b0 = float(self.b0_sel[:-1])

    def update_volumes_axis(self):
        """ 
        Update 'volumes' axis to use the frequency offsets in 
        graphs etc.
        
        Options should be handled much more cleanly than this!
        """
        freqs = self.freq_offsets.values()
        if self.ivm.main.ndim == 4 and len(freqs) == self.ivm.main.nvols:
            self.opts.t_combo.setCurrentIndex(1)
            self.opts.t_scale = self.freq_offsets.values()
            self.opts.sig_options_changed.emit(self)

    def new_pool(self):
        dlg = NewPoolDialog(self)
        if dlg.exec_():
            self.pools.append(dlg.pool(self.b0_sel))
            self.populate_poolgrid()

    def edit_pools(self):
        COL_HEADERS = ["PPM offset", "Exch rate", "T1", "T2"]
        enabled_pools = [p for p in self.pools if p.enabled]
        vals = [p.vals[self.b0_sel] for p in enabled_pools]
        names = [p.name for p in enabled_pools]
        d = GridEditDialog(self, vals, title="Edit Pools", 
                           col_headers=COL_HEADERS, row_headers=names, expandable=(False, False))
        if d.exec_():
            for pool, vals in zip(enabled_pools, d.table.values()):
                pool.vals[self.b0_sel] = vals
            self.custom_label.setText("Edited")
            self.poolvals_edited = True

    def reset_pools(self):
        self.custom_label.setText("")
        self.poolvals_edited = False
        for pool in self.pools:
            pool.reset()
            
    def get_rundata(self):
        # General defaults which never change
        rundata = {}
        rundata["data"] = self.data_combo.currentText()
        rundata["roi"] = self.roi_combo.currentText()
        rundata["model-group"] = "cest"
        rundata["noise"] = "white"
        rundata["max-iterations"] = "20"
        rundata["model"] = "cest"

        if self.output_rstar.isChecked():
            rundata["save-model-extras"] = ""
        if self.output_params.isChecked():
            rundata["save-mean"] = ""
        if self.output_modelfit.isChecked():
            rundata["save-model-fit"] = ""

        # Placeholders to be replaced with temp files
        rundata["pools"] = "pools.mat"
        rundata["ptrain"] = "ptrain.mat"
        rundata["spec"] = "dataspec.mat"
        
        if self.spatial_cb.isChecked():
            rundata["method"] = "spatialvb"
            rundata["param-spatial-priors"] = "MN+"
        else:
            rundata["method"] = "vb"
            rundata.pop("param-spatial-priors", None)
            
        prior_num = 1
        if self.t12_cb.isChecked():
            rundata["t12prior"] = ""
            if self.t1_cb.isChecked():
                rundata["PSP_byname%i" % prior_num] = "T1a"
                rundata["PSP_byname%i_type" % prior_num] = "I"
                rundata["PSP_byname%i_image" % prior_num] = self.t1_ovl.currentText()
                prior_num += 1

            if self.t2_cb.isChecked():
                rundata["PSP_byname%i" % prior_num] = "T2a"
                rundata["PSP_byname%i_type" % prior_num] = "I"
                rundata["PSP_byname%i_image" % prior_num] = self.t2_ovl.currentText()
                prior_num += 1
        else:
            rundata.pop("t12prior", None)

        if self.pvc_cb.isChecked():
            rundata["pvimg"] = self.pv_ovl.currentText()

        return rundata

    def update_ui(self):
        """ Update visibility / enabledness of widgets """
        self.pulsed = self.sat_combo.currentIndex() == 1
        self.st.spin.setVisible(not self.pulsed)
        self.st.label.setVisible(not self.pulsed)
        self.pds.setVisible(self.pulsed)
        self.pds_label.setVisible(self.pulsed)
        self.load_pds.setVisible(self.pulsed)
        self.pms.setVisible(self.pulsed)
        self.pms_label.setVisible(self.pulsed)
        self.load_pms.setVisible(self.pulsed)
        self.pr.spin.setVisible(self.pulsed)
        self.pr.label.setVisible(self.pulsed)
        self.t1_cb.setEnabled(self.t12_cb.isChecked())
        self.t2_cb.setEnabled(self.t12_cb.isChecked())
        self.t1_ovl.setEnabled(self.t12_cb.isChecked() and self.t1_cb.isChecked())
        self.t2_ovl.setEnabled(self.t12_cb.isChecked() and self.t2_cb.isChecked())
        self.pv_ovl.setEnabled(self.pvc_cb.isChecked())
        #self.unsat_combo.setEnabled(self.unsat_cb.isChecked())

    def get_dataspec(self):
        dataspec = ""
        freqs = self.freq_offsets.values()
        for idx, freq in enumerate(freqs):
            if self.pulsed:
                repeats = self.pr.spin.value()
            else:
                repeats = 1
            b1 = self.b1.spin.value()/1e6
            #if self.unsat_cb.isChecked():
            #    self.debug("Unsat", idx, self.unsat_combo.currentIndex())
            #    if idx == 0 and self.unsat_combo.currentIndex() in (0, 2):
            #        b1 = 0
            #    elif idx == len(freqs)-1 and self.unsat_combo.currentIndex() in (1, 2):
            #        b1 = 0
            dataspec += "%g %g %i\n" % (freq, b1, repeats)
        self.debug(dataspec)
        return dataspec

    def get_ptrain(self):
        ptrain = ""
        if self.pulsed:
            if not self.pms.valid() or not self.pms.valid():
                raise QpException("Non-numeric values in pulse specification")
            pms = self.pms.values()
            pds = self.pds.values()
            if len(pms) != len(pds):
                raise QpException("Pulse magnitude and duration must contain the same number of values")
            for pm, pd in zip(pms, pds):
                ptrain += "%g %g\n" % (pm, pd)
        else:
            ptrain += "1 %g\n" % self.st.spin.value()
        self.debug(ptrain)
        return ptrain

    def get_poolmat(self):
        poolmat = ""
        for pool in self.pools:
            vals = pool.vals[self.b0_sel]
            if pool.name == "Water":
                # Embed the B0 value in the top left
                vals = [self.b0 * GYROM_RATIO_BAR,] +vals[1:]
            if pool.enabled:
                poolmat += "\t".join([str(v) for v in vals]) + "\n"
        self.debug(poolmat)
        return poolmat

    def write_temp(self, name, data):
        f = tempfile.NamedTemporaryFile(prefix=name, delete=False)
        f.write(data.encode('utf-8')) 
        f.close()
        return f.name

    def batch_options(self):
        support_files = [("poolmat.mat", self.get_poolmat()),
                         ("dataspec.mat", self.get_dataspec()),
                         ("ptrain.mat", self.get_ptrain())]
        return "Fabber", self.get_rundata(), support_files

    def get_process_model(self):
        process = self.fabber_process(self.ivm)
        process.sig_finished.connect(self.postproc)
        return process

    def get_rundata_model(self):
        rundata = self.get_rundata()
        rundata["ptrain"] = self.write_temp("ptrain", self.get_ptrain())
        rundata["spec"] = self.write_temp("dataspec", self.get_dataspec())
        rundata["pools"] = self.write_temp("poolmat", self.get_poolmat())

        # Rename outputs using pool names rather than letters a, b, c etc
        renames = {"mean_M0a" : "mean_M0_Water", "mean_T1a" : "mean_T1_Water", "mean_T2a" : "mean_T2_Water"}
        for idx, pool in enumerate([p for p in self.pools[1:] if p.enabled]):
            pool_id = chr(ord('b') + idx)
            name = self.ivm.suggest_name(pool.name)
            renames["mean_M0%s_r" % pool_id] = "mean_M0_%s_r" % name
            renames["mean_k%sa" % pool_id] = "mean_exch_%s" % name
            renames["mean_ppm_%s" % pool_id] = "mean_ppm_%s" % name
            renames["mean_T1_%s" % pool_id] = "mean_T1_%s" % name
            renames["mean_T2_%s" % pool_id] = "mean_T2_%s" % name
            renames["cest_rstar_%s" % pool_id] = "cest_rstar_%s" % name
        rundata["output-rename"] = renames

        self.tempfiles = [rundata[s] for s in ("pools", "ptrain", "spec")]
        for item in rundata.items():
            self.debug("%s: %s" % item)
        return rundata

    def postproc(self, status, log, exception):
         # Remove temp files after run completes
        for fname in self.tempfiles:
            try:
                os.remove(fname)
            except:
                self.warn("Failed to delete temp file: %s" % fname)

        # Update 'volumes' axis to contain frequencies
        # FIXME removed as effectively requires frequencies to be
        # ordered and doesn't seem to look very good either
        #if status == Process.SUCCEEDED:
        #    self.update_volumes_axis()    

    def postproc_lda(self, status, log, exception):
        # Rename residuals and change sign convention
        residuals = self.ivm.data["residuals"]
        lorenz_diff = -residuals.raw()
        self.ivm.add(lorenz_diff, name="lorenz_diff", grid=residuals.grid, make_current=True)
        self.ivm.delete("residuals")

    def get_process_lda(self):
        # FIXME need special process to get the residuals only
        process = self.fabber_process(self.ivm)
        process.sig_finished.connect(self.postproc)
        process.sig_finished.connect(self.postproc_lda)
        return process
        
    def get_rundata_lda(self):
        rundata = self.get_rundata()
        rundata["ptrain"] = self.write_temp("ptrain", self.get_ptrain())
        rundata["spec"] = self.write_temp("dataspec", self.get_dataspec())
        
        # LDA is the residual data (data - modelfit)
        rundata.pop("save-mean", None)
        rundata.pop("save-zstat", None)
        rundata.pop("save-std", None)
        rundata.pop("save-model-fit", None)
        rundata.pop("save-model-extras", None)
        rundata["save-residuals"] = ""

        # Restrict fitting to parts of the z-spectrum with |ppm| <= 1 or |ppm| >= 30
        # This is done by 'masking' the timepoints so Fabber still reads in the
        # full data and still outputs a prediction at each point, however the
        # masked points are not used in the parameter fitting
        masked_idx = 1
        for idx, f in enumerate(self.freq_offsets.values()):
            if f < 0: f = -f
            if f > 1 and f < 30:
                rundata["mt%i" % masked_idx] = idx+1
                masked_idx += 1

        # Temporarily disable non-water pools just to generate the poolmat file
        enabled_pools = []
        for idx, p in enumerate(self.pools):
            if p.enabled:
                enabled_pools.append(p.name)
            p.enabled = (idx == 0)

        rundata["pools"] = self.write_temp("poolmat", self.get_poolmat())
        self.tempfiles = [rundata[s] for s in ("pools", "ptrain", "spec")]

        # Return pools to previous state
        for idx, p in enumerate(self.pools):
            p.enabled = (p.name in enabled_pools)

        for k in sorted(rundata.keys()):
            self.debug("%s: %s" % (k, rundata[k]))
        return rundata
