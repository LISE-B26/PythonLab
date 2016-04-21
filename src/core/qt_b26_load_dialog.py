"""
Basic gui class designed with QT designer
"""
import sip
sip.setapi('QVariant', 2)# set to version to so that the old_gui returns QString objects and not generic QVariants
from PyQt4 import QtGui, QtCore
from PyQt4.uic import loadUiType
from src.core import Parameter, Instrument, B26QTreeItem, ReadProbes, QThreadWrapper
import os.path
import numpy as np
import json as json, yaml
import yaml # we use this to load json files, yaml doesn't cast everything to unicode
from PySide.QtCore import QThread
from src.core.read_write_functions import load_b26_file
# from src.instruments import DummyInstrument
# from src.scripts import ScriptDummy, ScriptDummyWithQtSignal

import datetime
from collections import deque

from src.core import instantiate_probes, instantiate_scripts, instantiate_instruments

from src.scripts import ZISweeper, ZISweeperHighResolution, KeysightGetSpectrum, KeysightSpectrumVsPower, GalvoScan
from src.core.plotting import plot_psd
# from PyQt4.QtCore import QDataStream, Qt, QVariant

# load the basic old_gui either from .ui file or from precompiled .py file
try:
    # import external_modules.matplotlibwidget
    Ui_MainWindow, QMainWindow = loadUiType('load_dialog.ui') # with this we don't have to convert the .ui file into a python file!
except (ImportError, IOError):
    # load precompiled old_gui, to complite run pyqt_uic basic_application_window.ui -o basic_application_window.py
    from src.core.load_dialog import Ui_MainWindow
    from PyQt4.QtGui import QMainWindow
    print('Warning: on the fly conversion of .ui file failed, loaded .py file instead!!')



class LoadDialog(QMainWindow, Ui_MainWindow):
    DEFAULT_PATH = "Z:\Lab\Cantilever\Measurements\\__tmp"
    def __init__(self, type = "instruments"):
        """

        ControlMainWindow(intruments, scripts, probes)
            - intruments: depth 1 dictionary where keys are instrument names and keys are instrument classes
            - scripts: depth 1 dictionary where keys are script names and keys are script classes
            - probes: depth 1 dictionary where to be decided....?

        ControlMainWindow(settings_file)
            - settings_file is the path to a json file that contains all the settings for the old_gui

        Returns:

        """
        super(LoadDialog, self).__init__()
        self.setupUi(self)
        self.tree_infile_model = QtGui.QStandardItemModel()
        self.tree_infile.setModel(self.tree_infile_model)
        self.tree_infile_model.setHorizontalHeaderLabels(['Instrument', 'Value'])

        self.tree_loaded_model = QtGui.QStandardItemModel()
        self.tree_loaded.setModel(self.tree_loaded_model)
        self.tree_loaded_model.setHorizontalHeaderLabels(['Instrument', 'Value'])


        def connect_controls():
            self.btn_open.clicked.connect(lambda: self.open_file_dialog(self.txt_probe_log_path))

        connect_controls()


    def open_file_dialog(self, target):
        # sender = self.sender()
        # self.file_dialog_open = True
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Select a file:', self.DEFAULT_PATH)
        target.setText(filename)

        input_dict = load_b26_file(filename)['instruments']

        self.fill_tree(self.tree_infile,input_dict )

    # QtGui.QTreeWidgetItem
    def fill_tree(self, tree, input_dict):
        """
        fills a tree with nested parameters
        Args:
            tree: QtGui.QTreeWidget
            parameters: dictionary or Parameter object

        Returns:

        """
        for index, (instrument, instrument_settings) in enumerate(input_dict.iteritems()):
            item = QtGui.QStandardItem(instrument)

            for key, value in instrument_settings['settings'].iteritems():
                child_name = QtGui.QStandardItem(key)
                child_name.setDragEnabled(False)
                child_value = QtGui.QStandardItem(unicode(value))
                child_value.setDragEnabled(False)
                item.appendRow([child_name, child_value])
            tree.model().appendRow(item)

            tree.setFirstColumnSpanned(index, self.tree_infile.rootIndex(), True)



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ex = LoadDialog()

    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
