import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QPushButton, QComboBox, QHBoxLayout

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'addAttribute.ui'))


class AddAttribute(QDialog, FORM_CLASS):
    def __init__(self, iface, dataInsert):
        """Constructor."""

        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.database = dataInsert
        self.currentAtribute = ''
        self.currentAtribute = []

    def prepareTela(self):
        pass
        self.database = self.dataInsert
        self.currentAtribute = ""

    def createCodeLinstBolean(self):
        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem("True")
        self.cb.addItem("false")
        layout.addWidget(self.cb)
        self.setLayout(layout)


    def createWindowsString(self):
        a =1


    def createWindowsInt(self):
        a=1
        #ODO:
    def createWindowsCodeList(self, className):


        a=1
