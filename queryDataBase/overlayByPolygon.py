# -*- coding: utf-8 -*-
"""
/***************************************************************************
OverlayByPolygon
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
import sys

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'overlayByPolygon.ui'))

from ..configuration.configurationDialog import ConfigurationDialog
from .resultQuery import ResultQuery
from ..dbTools.dbTools import DbTools


class OverlayByPolygon(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""
        #super(EspuConsulteDialog, self).__init__(parent)
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface

        self.nameConect = ConfigurationDialog.getLastNameConnection(self)
        (self.host,self.port, self.db, self.user, self.password) = ConfigurationDialog.getServerConfiguration(self, self.nameConect)
        self.searchDB.clicked.connect(self.executeQueryOnMode)
        self.radioButtonFeatureSelec.clicked.connect(self.abilitFileWidget)
        self.radioButtonFromFile.clicked.connect(self.abilitFileWidget)
        self.back.clicked.connect(self.close)
        self.ignoreTable = ["unidade_federacao", "municipio"]

        #super(EspuConsulteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        # self.generateReport.clicked.connect(self.generatorReport)

    def abilitFileWidget(self):

        """Control of radio button."""

        if self.radioButtonFromFile.isChecked():
            self.mQgsFileWidget.setEnabled(True)
        if not self.radioButtonFromFile.isChecked():
            self.mQgsFileWidget.setEnabled(False)


    def trasformSelctLayerToWkb(self):

        """Traform a select Layer to WKB format. """

        currentLayer = self.iface.mapCanvas().currentLayer()
        selectedFeatures = len(currentLayer.selectedFeatures())

        selectedFeature = currentLayer.selectedFeatures()[0]
        d = selectedFeature.geometry().asWkb()
        return d

    def trasformSelctLayerToWkt(self):

        """Traform a select Layer to WKT format."""

        currentLayer = self.iface.mapCanvas().currentLayer()
        selectedFeatures = len(currentLayer.selectedFeatures())
        selectedFeature = currentLayer.selectedFeatures()[0]
        d = selectedFeature.geometry().asWkt()
        return d


    def calculateOverlaps(self):

        """Calculates overlays with a selected feature."""

        currentLayer = self.iface.mapCanvas().currentLayer()
        selectedFeatures = len(currentLayer.selectedFeatures())
        dbt=DbTools()
        tablesGeo = dbt.getTablesGeo(schemaName='public') #depois mudar para view 'faixa_seguranca'
        tablesGeoColumns = dbt.getTablesCollumnsAll(tablesGeo,'public')

        for i in range(0,len(self.ignoreTable)):
            tablesGeo.remove(self.ignoreTable[i])

        #rows = dbt.getTablesGeo(schemaName='public')
        #rows = dbt.getTableColum ('area_especial', 'public')
        #rows = dbt.generateId('area_especial', 'public', 'MG')
        #print (rows)
        #rows = dbt.calculateIntersect(self.trasformSelctLayerToWkt(), 'area_especial')
        #for r in rows:
        #    print (r)

        #inicializando o progress Bar
        self.progressBar.setEnabled(True)
        self.progressBar.setValue(0)
        self.labelStatusProgress.setText('Iniciando Verificação')
        self.labelStatusProgress.setEnabled(True)
        porcentProgress = 100/(int(len(tablesGeo)) + 2)
        acumuladoProgresso = 0
        count = 0
        results={}

        if currentLayer:
            if selectedFeatures == 1:
                try:
                    #print (self.nameConect)
                    #print (self.host,self.port, self.db, self.user, self.password)
                    #conn = psycopg2.connect(" dbname=" + self.db + " user=" + self.user + " host=" + self.host+ " password=" + self.password )
                    #if conn:

                    print ("FOI!")
                    print(tablesGeo)
                    pol = self.trasformSelctLayerToWkt()
                    self.labelStatusProgress.setText('Obtendo a : ' + 'Unidade da Federacao' )
                    ufIntecectList = dbt.calculateIntersect(pol, "unidade_federacao")
                    acumuladoProgresso= acumuladoProgresso+ porcentProgress
                    self.labelStatusProgress.setText('Obtendo o : ' + 'municipio' )
                    municipioInterctList = dbt.calculateIntersect(pol, "municipio")
                    acumuladoProgresso= acumuladoProgresso+ porcentProgress

                    for table in tablesGeo:
                        count =count+1
                        self.labelStatusProgress.setText('Verificando em: ' + table )
                        result = dbt.calculateIntersect(pol, table)

                        if len(result)!=0:
                            results.update({table:result})
                        result = []

                        acumuladoProgresso= acumuladoProgresso+ porcentProgress
                        self.progressBar.setValue(acumuladoProgresso)

                        if count == int(len(tablesGeo)):
                            self.progressBar.setValue(100)
                            self.labelStatusProgress.setText('Verificação Finalizada!' )

                    #print (results)
                        #ADD FUNCAO PARA CALCULO
                        #ADD FANDACAO
                except:
                    print (sys.exc_info()[0])
                    print ("I am unable to connect to the database")
            else:
                QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("One and only one feature must be selected to perform the calculations."))
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, open a layer and select a line or polygon feature."))

        if results:
            self.generatorReport(results, tablesGeoColumns, ufIntecectList, municipioInterctList)

    def executeQueryOnMode(self):
        if self.radioButtonFeatureSelec.isChecked():
            self.calculateOverlaps()


    def generatorReport(self, results, tablesGeoColumns, ufIntecectList, municipioInterctList):

        """Generates a summary report of the result of the query"""

        d=ResultQuery(self.iface, results, tablesGeoColumns, ufIntecectList, municipioInterctList)
        d.fillTable()
        d.exec_()