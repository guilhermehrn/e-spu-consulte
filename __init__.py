# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EspuConsulte
                                 A QGIS plugin
 Consulta Sobreposição com áreas do Governo Federal do Brasil
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-11-12
        copyright            : (C) 2018 by Guilherme Henrique
        email                : guilherme.nascimento@planejamento.gov.br
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

from __future__ import absolute_import

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load EspuConsulte class from file EspuConsulte.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .e_spu_consulte import EspuConsulte
    return EspuConsulte(iface)
