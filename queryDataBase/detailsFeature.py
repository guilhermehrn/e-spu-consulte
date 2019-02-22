# -*- coding: utf-8 -*-
"""
/***************************************************************************
detailsFeature
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


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QPushButton

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'detailsFeature.ui'))



class DetailsFeature(QDialog, FORM_CLASS):
    """Show windows with details of the feature"""
    def __init__(self, iface, feicaodata, tableColumns):
        """Constructor."""

        QDialog.__init__(self)
        self.setupUi(self)
        self.tableColumns = tableColumns
        self.feicaoData = feicaodata
        self.iface = iface

    def detailsFeaturesAll(self):

        print("olha iss aqui: ",self.tableColumns)
        
        if self.tableWidgetDetails.rowCount() == 0:
            self.tableWidgetDetails.setRowCount(len(self.tableColumns))

        for i in range(0, len(self.tableColumns)):
            itemCell = QTableWidgetItem(str(self.tableColumns[i]))
            print(itemCell)
            self.tableWidgetDetails.setItem(i, 0, itemCell)

            print(self.feicaoData[0][i])
            itemCell = QTableWidgetItem(str(self.feicaoData[0][i]))
            #print(itemCell)
            self.tableWidgetDetails.setItem(i, 1, itemCell)
