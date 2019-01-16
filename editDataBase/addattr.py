import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QPushButton

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attblooleanExt.ui'))



class Addattr(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""

        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
