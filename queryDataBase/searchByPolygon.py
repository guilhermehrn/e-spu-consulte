# -*- coding: utf-8 -*-
"""
/***************************************************************************
seachByPolygon
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
    os.path.dirname(__file__), 'searchByPolygon.ui'))

from ..configuration.configurationDialog import ConfigurationDialog
from ..dbTools.dbTools import DbTools


class SearchByPolygon(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""
        #super(EspuConsulteDialog, self).__init__(parent)
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface

        self.nameConect = ConfigurationDialog.getLastNameConnection(self)
        (self.host,self.port, self.db, self.user, self.password) = ConfigurationDialog.getServerConfiguration(self, self.nameConect)
        self.searchDB.clicked.connect(self.calcularIntercecoesPorFeicaoSelec)

        #super(EspuConsulteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        # self.generateReport.clicked.connect(self.generatorReport)


    def trasformSelctLayerToWkb(self):

        currentLayer = self.iface.mapCanvas().currentLayer()
        selectedFeatures = len(currentLayer.selectedFeatures())

        selectedFeature = currentLayer.selectedFeatures()[0]
        d = selectedFeature.geometry().asWkb()
        #print (d)
        return d

    def trasformSelctLayerToWkt(self):

        currentLayer = self.iface.mapCanvas().currentLayer()
        selectedFeatures = len(currentLayer.selectedFeatures())

        selectedFeature = currentLayer.selectedFeatures()[0]
        d = selectedFeature.geometry().asWkt()
        #print (d)
        return d




    def calcularIntercecoesPorFeicaoSelec(self):
        currentLayer = self.iface.mapCanvas().currentLayer()
        selectedFeatures = len(currentLayer.selectedFeatures())

        dbt=DbTools()

        rows = dbt.getTablesGeo(schemaName='public')
        #rows = dbt.getTableColum ('area_especial', 'public')
        #rows = dbt.generateId('area_especial', 'public', 'MG')
        #print (rows)
        #rows = dbt.calculateIntersect(self.trasformSelctLayerToWkt(), 'area_especial')
        for r in rows:
            print (r)



        # if currentLayer:
        #     if selectedFeatures == 1:
        #         poligonBin = self.trasformSelctLayerToWkb()
        #         try:
        #             print (self.nameConect)
        #             print (self.host,self.port, self.db, self.user, self.password)
        #             conn = psycopg2.connect(" dbname=" + self.db + " user=" + self.user + " host=" + self.host+ " password=" + self.password )
        #             if conn:
        #                 print ("FOI!")
        #                 #ADD FUNCAO PARA CALCULO
        #                 #ADD FANDACAO
        #         except:
        #             print ("I am unable to connect to the database")
        #     else:
        #         QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("One and only one feature must be selected to perform the calculations."))
        # else:
        #     QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, open a layer and select a line or polygon feature."))



    # def generatorReport(self):
    #     d=ConfigurationDialog(self.iface)
    #     d.exec_()
