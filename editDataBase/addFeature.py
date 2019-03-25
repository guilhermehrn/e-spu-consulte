import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QPushButton
from .addAttribute import AddAttribute
from .selectTable import SelectTable
from ..dbTools.dbTools import DbTools

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'addFeature.ui'))



class AddFeature(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""

        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.dataInsert = {}

        self.radioButtonObjetoSelecAddFeature.clicked.connect(self.radioButtonControl)
        self.radioButtonFromFileAddFeature.clicked.connect(self.radioButtonControl)
        self.nextScreen.clicked.connect(self.enterAtributo)
        self.tablesGeo = DbTools().getTablesGeo("public")

    def radioButtonControl(self):
        if self.radioButtonFromFileAddFeature.isChecked():
            self.mQgsFileWidget.setEnabled(True)
        if not self.radioButtonFromFileAddFeature.isChecked():
            self.mQgsFileWidget.setEnabled(False)

    def enterAtributo(self):
        d=SelectTable(self.iface, self.tablesGeo,self.dataInsert)
        self.close()
        d.exec_()
