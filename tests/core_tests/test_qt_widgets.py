from unittest import TestCase

import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
import sys
from src.core.qt_widgets import B26QTreeItem,B26QTreeWidget
from src.core import Parameter

class UI(QtGui.QMainWindow):

    def __init__(self, parameters = None, parent=None):

        ## Init:
        super(UI, self).__init__( parent )

        # ----------------
        # Create Simple UI with QTreeWidget
        # ----------------
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)

        self.parameters = parameters

        self.treeWidget = B26QTreeWidget(self.centralwidget, self.parameters)

        # self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.treeWidget)
        self.setCentralWidget(self.centralwidget)

        # ----------------
        # Set TreeWidget Headers
        # ----------------
        HEADERS = ( "parameter", "value" )
        self.treeWidget.setColumnCount( len(HEADERS) )
        self.treeWidget.setHeaderLabels( HEADERS )


        # ----------------
        # Add Custom QTreeWidgetItem
        # ----------------
        self.treeWidget.itemChanged.connect(lambda: self.update_parameters(self.treeWidget, self.parameters))

        # shot down
        print('close')
        self.close()

class TestB26QTreeWidget(TestCase):
    def test_create_widget_parameters(self):


        parameters = Parameter([
            Parameter('test1', 0, int, 'test parameter (int)'),
            Parameter('test2' ,
                      [Parameter('test2_1', 'string', str, 'test parameter (str)'),
                       Parameter('test2_2', 0.0, float, 'test parameter (float)'),
                       Parameter('test2_3', 'a', ['a', 'b', 'c'], 'test parameter (list)'),
                       Parameter('test2_4', False, bool, 'test parameter (bool)')
                       ]),
            Parameter('test3', 'aa', ['aa', 'bb', 'cc'], 'test parameter (list)'),
            Parameter('test4', False, bool, 'test parameter (bool)')
        ])

        app = QtGui.QApplication(sys.argv)
        ex = UI(parameters)
        # sys.exit(app.exec_())



    def test_create_widget_parameters(self):


        parameters = {
            'test1':0,
            'test2':{'test2_1':'ss', 'test3':4},
            'test4':0
        }

        app = QtGui.QApplication(sys.argv)
        ex = UI(parameters)
        # sys.exit(app.exec_())
