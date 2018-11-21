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
import psycopg2

from PyQt5 import uic
from PyQt5 import QtWidgets
import psycopg2


from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMessageBox, QDialog
from ..configuration.configurationDialog import ConfigurationDialog


class DbTools(QDialog, FORM_CLASS):
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
        try:
            print (self.nameConect)
            print (self.host,self.port, self.db, self.user, self.password)
            self.conn = psycopg2.connect(" dbname=" + self.db + " user=" + self.user + " host=" + self.host+ " password=" + self.password )
        except:
            print ("I am unable to connect to the database")

    #Return a table with relation "FOREIGN KEY". The format of table is: FK_Table | FK_Column | PK_Table | PK_Column
    def getForeignKeyRelationTable(self, tableName):
        sql='SELECT conrelid::regclass AS ' + '"FK_Table"'+
        ',CASE WHEN pg_get_constraintdef(c.oid) LIKE' + " 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), 14, position(')' in pg_get_constraintdef(c.oid))-14) END AS " +' "FK_Column"''+
        ',CASE WHEN pg_get_constraintdef(c.oid) LIKE' + " 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), position(' REFERENCES ' in pg_get_constraintdef(c.oid))+12, position('(' in substring(pg_get_constraintdef(c.oid), 14))-position(' REFERENCES ' in pg_get_constraintdef(c.oid))+1) END AS " + '"PK_Table"'+
        ',CASE WHEN pg_get_constraintdef(c.oid) LIKE' + " 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), position('(' in substring(pg_get_constraintdef(c.oid), 14))+14, position(')' in substring(pg_get_constraintdef(c.oid), position('(' in substring(pg_get_constraintdef(c.oid), 14))+14))-1) END AS" + '"PK_Column"'+
        "FROM   pg_constraint c" +
        "JOIN   pg_namespace n ON n.oid = c.connamespace"+
        "WHERE  contype IN ('f', 'p ')" +
        "AND pg_get_constraintdef(c.oid) LIKE 'FOREIGN KEY %' AND conrelid::regclass::text='" + tableName + "'" +
        "ORDER  BY pg_get_constraintdef(c.oid), conrelid::regclass::text, contype DESC;"

        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    #Return a RSID of the table. Return a table
    def getSridTable(self, tableName):
        sql = "select ST_SRID(ta.geom) as srid from" tableName +" as ta group by srid"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        srid = ''
        for row in rows:
            srid = row[0]

        return srid


    #return all table of a schema.
    def getTables(self, schemaName):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='" + schemaName + "';"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def calculateIntersect(self, polygono, tableName):
        srid = self.getSridTable(tableName)
        sql = "select * from" + tableName + " as ta where ST_Intersects (ta.geom," + "'SRID=" + srid + ";" + polygono + "'::geometry)"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def getTable(self, tableName, schemaName):
        sql = "select * from " + schemaName + "." + tableName +";"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
