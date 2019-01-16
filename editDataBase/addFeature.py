import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QPushButton
from .addattr import Addattr

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'addFeature.ui'))



class AddFeature(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""

        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.nextScreen.clicked.connect(self.enterAtributo)
        

    def enterAtributo(self):
        d=Addattr(self.iface)
        d.exec_()
