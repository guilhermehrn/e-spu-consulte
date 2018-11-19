# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EspuConsulteDialog
                                 A QGIS plugin
 Consulta Sobreposição com áreas do Governo Federal do Brasil
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Guilherme Henrique
        email                : guilherme.nascimento@planejamento.gov.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import uic
from PyQt5 import QtWidgets
import psycopg2


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'queryDataBase.ui'))

from .resultQuery import ResultQuery
from ..configuration.configurationDialog import ConfigurationDialog

class QueryDataBase(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""

        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        #super(EspuConsulteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.nameConect = ConfigurationDialog.getLastNameConnection(self)

        (self.host,self.port, self.db, self.user, self.password) = ConfigurationDialog.getServerConfiguration(self, self.nameConect)



        self.iniciar.clicked.connect(self.trasformSelctLayerToWkb)



    def trasformSelctLayerToWkb(self):
        currentLayer = self.iface.mapCanvas().currentLayer()
        if currentLayer:
            selectedFeatures = len(currentLayer.selectedFeatures())
            if selectedFeatures == 1:
                selectedFeature = currentLayer.selectedFeatures()[0]
                d = selectedFeature.geometry().asWkb()
                print (d)
            else:
                QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("One and only one feature must be selected to perform the calculations."))
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, open a layer and select a line or polygon feature."))


    def queryFromVectorObject(self):
        try:
            conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
        except:
            print ("I am unable to connect to the database")


    def showResult(self):
        d=ResultQuery(self.iface)
        d.exec_()


#https://github.com/skeenp/QGIS3-getWKT/blob/master/getwkt3.py
#https://qgis.org/api/classQgsGeometry.html
