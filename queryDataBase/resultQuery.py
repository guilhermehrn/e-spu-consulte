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
from PyQt5 import QtGui
from PyQt5 import QtCore

from qgis.core import QgsVectorLayer, QgsField, QgsFeature
from PyQt5.QtCore import QVariant, QByteArray
from qgis.core import QgsGeometry, QgsPointXY, QgsVectorFileWriter, QgsCoordinateReferenceSystem

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QPushButton
from .detailsFeature import DetailsFeature

import psycopg2
from osgeo import ogr
from qgis.core import QgsVectorLayer, QgsPoint, QgsFeature, QgsGeometry,QgsPointXY, QgsProject
from ..dbTools.dbTools import DbTools


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'resultQuery.ui'))



class ResultQuery(QDialog, FORM_CLASS):
    def __init__(self, iface, results, tablesGeoColumns,ufIntecectList, municipioInterctList):
        """Constructor."""

        QDialog.__init__(self)
        self.setupUi(self)
        self.resultDic = results
        self.tablesGeoColumns = tablesGeoColumns
        self.iface = iface
        self.columnConstats = {'integer': 2, 'real': 6, 'boolean':1, 'text': 79, 'character varying': 10}
        #self.generateLayers.clicked.connect(self.createLayer)
        #super(EspuConsulteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.generateLayers.clicked.connect(self.generateVisualization)
        # self.generateReport.clicked.connect(self.generatorReport)

    def calculcateNumberLines(self):
        t = self.resultDic.keys()
        numbLinesPrev = 0
        keysClass = [*t]
        for classe in keysClass:
            aux = len(self.resultDic[classe])
            numbLinesPrev = numbLinesPrev + aux

        return numbLinesPrev

    def detalharResultado(self):
        #button = QtGui.qApp.focusWidget()
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        if index.isValid():
            if index.column() == 4:
                classFeicao = str(self.tableWidget.item(index.row(), 2).text())
                #print(classFeicao)
                tablesResult = self.resultDic[classFeicao]
                d = DetailsFeature(self.iface, tablesResult, self.tablesGeoColumns[classFeicao])
                d.detailsFeaturesAll()
                d.exec_()
                #print(tablesResult[self.IndexTableToResult[index.row()][2]])

    def temColuna(self,className,columnName):
        keyColumns = self.tablesGeoColumns[className]
        d=False

        for kCol in keyColumns:
            if kCol == columnName:
                d=True

        return d

    def createLayer(self):

        dbt = DbTools()
        key = [*self.resultDic.keys()]
        i = createLayer
        #print (self.resultDic)
        for classe in self.resultDic:
            geomType = dbt.getGeomTypeTable(key[i])
            url = geomType+"?crs=epsg:4674"
            vl = QgsVectorLayer(url, "temporary" + geomType, "memory")
            pr = vl.dataProvider()
            vl.startEditing()

            colDataType = dbt.getDataTypeColumns(key[i])

            attr = []
            columnGeom = self.tablesGeoColumns[key[i]]
            geomIndex = columnGeom.index('geom')
            columnNoGeom = columnGeom
            columnNoGeom.remove("geom")
            # print (columnGeom)

            for column in columnGeom:
                #costType = colDataType[column][0]
                if column != 'geom':
                    attr.append(QgsField(column, 10))

            pr.addAttributes(attr)

            # add a feature


            attrValue = {}
            for row in self.resultDic[classe]:
                print (type(row))
                fet = QgsFeature()
                buf = QByteArray(row[geomIndex].encode())
                print (type(QgsGeometry.fromWkb(buf)))
                #fet.setGeometry(self.QgsGeometry.fromWkb(row[geomIndex]))
                # for c in range(0,len(row)):
                #     attrValue.update

            i = i+1

        # vl = QgsVectorLayer("Point", "temporary_points", "memory")
        # pr = vl.dataProvider()
        #
        # # Enter editing mode
        # vl.startEditing()
        #
        # # add fields
        # pr.addAttributes( [ QgsField("name", QVariant),
        #         QgsField("age",  QVariant.Int),
        #         QgsField("size", QVariant.Double) ] )
        #
        #         # add a feature
        # fet = QgsFeature()
        # fet.setGeometry( QgsGeometry.fromPointXY(QgsPointXY(10.0,10.0)) )
        # # fet.setAttribute( { 0 : QVariant("Johny"), 1 : QVariant(20), 2 : QVariant(0.3) } )
        # fet.setAttributes( [QVariant("Johny"),QVariant(20),QVariant(0.3)])
        # pr.addFeatures( [ fet ] )
        #
        # # Commit changes
        #
        # vl.updateExtents()
        # # layer = self.iface.addVectorLayer(vl, "My Layer", "ogr")
        # # if not layer:
        # #     print("Layer failed to load!")
        # path = os.path.join(os.path.dirname(__file__), 'data/my_shapes.shp')
        #
        # vl.commitChanges()
        # error = QgsVectorFileWriter.writeAsVectorFormat(vl,path, "utf-8", QgsCoordinateReferenceSystem(4326), "ESRI Shapefile")
        #
        # if error == QgsVectorFileWriter.NoError:
        #     print("success!")
        #
        # layer = self.iface.addVectorLayer(path, "My Layer", "ogr")
        # if not layer:
        #     print("Layer failed to load!")

    def fillTable(self):

        if self.tableWidget.rowCount() == 0:
            self.tableWidget.setRowCount(self.calculcateNumberLines())

        i=0
        t = self.resultDic.keys()
        keysClass = [*t]
        self.IndexTableToResult=[]

        print (keysClass)
        if len(self.resultDic) > 0:
            for classe in keysClass:
                print ("Oi: " + classe)
                MatrizFeicoes = self.resultDic[classe]
                keyColumns = self.tablesGeoColumns[classe]
                print (keyColumns)

                if self.temColuna(classe,"idproduto"):
                    idIndex = keyColumns.index("idproduto")
                else:
                    idIndex = keyColumns.index("terra_originalmente_uniao_idproduto")

                if self.temColuna(classe,"nome"):
                    nomeIndex = keyColumns.index("nome")
                else:
                    nomeIndex = -1

                if self.temColuna(classe,"observacao"):
                    ObsIndex = keyColumns.index("observacao")
                else:
                    ObsIndex= -1

                j=0
                for feicao in MatrizFeicoes:
                    #print(MatrizFeicoes[j][idIndex])
                    if idIndex > -1:
                        itemCellClass = QTableWidgetItem(str(MatrizFeicoes[j][idIndex]))
                        self.tableWidget.setItem(i, 0, itemCellClass)

                    if nomeIndex > -1:
                        itemCellClass = QTableWidgetItem(str(MatrizFeicoes[j][nomeIndex]))
                        self.tableWidget.setItem(i, 1, itemCellClass)

                    if ObsIndex > -1:
                        itemCellClass = QTableWidgetItem(str(MatrizFeicoes[j][ObsIndex]))
                        self.tableWidget.setItem(i, 3, itemCellClass)

                    itemCellClass = QTableWidgetItem(classe)
                    self.tableWidget.setItem(i, 2, itemCellClass)
                    self.IndexTableToResult.append((i,classe,j))

                    self.btn = QPushButton(self.tableWidget)
                    self.btn.setText("...")
                    self.btn.setObjectName("tbt"+str(i))
                    self.btn.clicked.connect(self.detalharResultado)

                    self.tableWidget.setCellWidget(i, 4, self.btn)
                    self.tableWidget.itemClicked.connect(self.detalharResultado)
                    j=j+1
                    i=i+1

    def generateVisualization(self):
        keys = [*self.resultDic.keys()]

        for key in keys:

            tableResult = self.resultDic[key]
            colunaCount = len(tableResult[0])
            strWktIndex= colunaCount-1
            colNames = self.tablesGeoColumns[key]

            geomType = ogr.CreateGeometryFromWkt(tableResult[0][strWktIndex]).GetGeometryName()

            layer = QgsVectorLayer(geomType + '?crs=epsg:4674', 'interc_' + key , 'memory')
            prov = layer.dataProvider()

            QgsFildsList = []

            for col in colNames:
                QgsFildsList.append(QgsField(col, QVariant.String))


            prov.addAttributes(QgsFildsList)
            layer.updateFields()


            for row in tableResult:

                strWkt = row[strWktIndex]
                geo=ogr.CreateGeometryFromWkt(strWkt)
                #print ("Oi: ", list(row).pop())

                r = list(row)
                r.pop()
                feat = QgsFeature()
                feat.setGeometry(QgsGeometry.fromWkt(strWkt))
                #feat.setAttributes("nome", "end")
                feat.setAttributes (r)
                prov.addFeatures([feat])
                layer.updateExtents()
                QgsProject.instance().addMapLayer(layer)

    def generatePointLayer(self, pointText, attr):

        layer = QgsVectorLayer('point?crs=epsg:4674', 'Ponto_endereco', 'memory')
        prov = layer.dataProvider()
        feat = QgsFeature()
        QgsFildsList = []
        QgsFildsList.append(QgsField("Endereço", QVariant.String))
        prov.addAttributes(QgsFildsList)

        layer.updateFields()
        print(pointText)

        feat.setGeometry(QgsGeometry.fromWkt(pointText[0][0]))
        feat.setAttributes([attr])
        prov.addFeatures([feat])

        layer.updateExtents()
        QgsProject.instance().addMapLayer(layer)
