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


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'e_spu_consulte_dialog_base.ui'))

from .configuration.configurationDialog import ConfigurationDialog
#from .queryDataBase.queryDataBase import QueryDataBase
from .queryDataBase.searchByPolygon import SearchByPolygon
from .queryDataBase.searchByPoint import SearchByPoint

class EspuConsulteDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self,iface, parent=None):
        """Constructor."""
        super(EspuConsulteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)
        self.iface = iface
        self.consultSobreposicao.clicked.connect(self.consultarSobreposicao)
        self.consultBase.clicked.connect(self.consultarPorEndereco)
        self.configuracoes.clicked.connect(self.setConfigurations)



    def setConfigurations(self):
        d=ConfigurationDialog(self.iface)
        d.exec_()

    def consultarSobreposicao(self):
        d=SearchByPolygon(self.iface)
        d.exec_()

    def consultarPorEndereco(self):
        d= SearchByPoint(self.iface)
        d.exec_()
