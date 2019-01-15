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
from ..configuration.configurationDialog import ConfigurationDialog


class DbTools(QDialog):
    def __init__(self):
        """Constructor."""

        QDialog.__init__(self)
        #self.setupUi(self)
        #self.iface = iface
        #super(DbTools, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.dataGeomTypes = {"trecho_rodoviario":"LineString", "trecho_ferroviario":"LineString", "area_politico_adminitrativo":"Polygon", "unidade_federacao":"Polygon", "municipio": "Polygon", "municipio":"Polygon", "terreno_sujeito_inundacao":"Polygon","faixa_dominio":"Polygon", "parcela":"Polygon", "terra_originalmente_uniao":"Polygon","trecho_terreno_marginal":"Polygon", "trecho_terreno_marginal":"Polygon","trecho_area_indubitavel":"Polygon", "terras_interiores":"Polygon", "faixa_dominio":"Polygon", "area_especial":"Polygon", "massa_dagua":"Polygon"}
        self.nameConect = ConfigurationDialog.getLastNameConnection(self)
        (self.host,self.port, self.db, self.user, self.password) = ConfigurationDialog.getServerConfiguration(self, self.nameConect)
        # try:
        print (self.nameConect)
        print (self.host,self.port, self.db, self.user, self.password)
        self.conn = psycopg2.connect(" dbname=" + self.db + " user=" + self.user + " host=" + self.host+ " password=" + self.password )
    # except:
                # print ("I am unable to connect to the database")

    #Return a table with relation "FOREIGN KEY". The format of table is: FK_Table | FK_Column | PK_Table | PK_Column
    def getForeignKeyRelationTable(self, tableName):
        sql='SELECT conrelid::regclass AS ' + '"FK_Table"'
        + ',CASE WHEN pg_get_constraintdef(c.oid) LIKE' + " 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), 14, position(')' in pg_get_constraintdef(c.oid))-14) END AS " +' "FK_Column"'
        +',CASE WHEN pg_get_constraintdef(c.oid) LIKE' + " 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), position(' REFERENCES ' in pg_get_constraintdef(c.oid))+12, position('(' in substring(pg_get_constraintdef(c.oid), 14))-position(' REFERENCES ' in pg_get_constraintdef(c.oid))+1) END AS " + '"PK_Table"'
        +',CASE WHEN pg_get_constraintdef(c.oid) LIKE' + " 'FOREIGN KEY %' THEN substring(pg_get_constraintdef(c.oid), position('(' in substring(pg_get_constraintdef(c.oid), 14))+14, position(')' in substring(pg_get_constraintdef(c.oid), position('(' in substring(pg_get_constraintdef(c.oid), 14))+14))-1) END AS" + '"PK_Column"'
        +"FROM   pg_constraint c"
        +"JOIN   pg_namespace n ON n.oid = c.connamespace"
        +"WHERE  contype IN ('f', 'p ')"
        +"AND pg_get_constraintdef(c.oid) LIKE 'FOREIGN KEY %' AND conrelid::regclass::text='" + tableName + "'"
        +"ORDER  BY pg_get_constraintdef(c.oid), conrelid::regclass::text, contype DESC;"

        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    #Return a RSID of the table. Return a table
    def getSridTable(self, tableName):
        sql = "select ST_SRID(ta.geom) as srid from " + tableName +" as ta group by srid"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        srid =''
        for row in rows:
            srid = row[0]

        return srid

    def getNumberLineOfTable(self, tableName):
        sql = "select count(*) from " + tableName
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        numberLine=''

        for row in rows:
            numberLine = row[0]
        return numberLine

    #return all table of a schema. Return a list of strings
    def getAllTables(self, schemaName):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='" + schemaName + "';"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        geoTablesLis = []
        for r in rows:
            geoTablesLis.append(r[0])

        return geoTablesLis
        #SELECT * FROM information_schema.tables WHERE table_schema='public' AND table_type = 'BASE TABLE' AND table_name<>'spatial_ref_sys'
        #SELECT * FROM  information_schema.columns where table_schema='public' AND column_name='geom'

    #return all table with geometry. Return a list of strings
    def getTablesGeo(self, schemaName):
        sql = "SELECT * FROM  information_schema.columns where table_schema='" + schemaName + "' AND column_name='geom'"
        #sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='" + schemaName + "';"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        geoTablesLis = []
        for r in rows:
            geoTablesLis.append(r[2])

        return geoTablesLis

    #return a table with intersects with  polygono
    def calculateIntersect(self, polygono, tableName):
        t = []
        if self.getNumberLineOfTable(tableName) > 0:
            srid = self.getSridTable(tableName)
            sql = "select * from " + tableName + " as ta where ST_Intersects (ta.geom, " + "ST_GeogFromText('SRID=" + str(srid) + ";" + polygono + "'))"

            cur = self.conn.cursor()

            cur.execute(sql)
            rows = cur.fetchall()
            # for r in rows:
            #     print (r[0])
            return rows
        else:
            return t

    #return a array with columns names of a table.
    def getTableColum(self, tableName, schemaName):
        sql = "select column_name from INFORMATION_SCHEMA.columns where table_schema= '" + schemaName + "' and table_name= '" + tableName + "';"
        #sql = "select * from " + schemaName + "." + tableName +";"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columnsLis = []
        for r in rows:
            columnsLis.append(r[0])
        return columnsLis

    #return dicionario.
    def getTablesCollumnsAll(self, tablesList, schemaName):
        columnsList=[]
        tablesCollumnsDic={}
        for table in tablesList:
            columnsList = self.getTableColum(table, schemaName)
            tablesCollumnsDic.update({table:columnsList})

        return tablesCollumnsDic

    def getGeomTypeTable(self, tableName):
        return self.dataGeomTypes[tableName]


    def getDataTypeColumns(self, tableName):
        sql = "select column_name, data_type, character_maximum_length from information_schema.columns where table_name='" + tableName + "'"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        typeCollumnsDic={}
        for row in rows:
            typeCollumnsDic.update({row[0]:(row[1],row[2])})

        return typeCollumnsDic




    def generateId(self,tableName, schemaName, siglaUf):
        codeClassDic= {"trecho_rodoviario":1, "trecho_ferroviario":2, "area_politico_adminitrativo":3, "unidade_federacao":3, "municipio": 3, "municipio":4, "terreno_sujeito_inundacao":5,"faixa_dominio":6, "parcela":7, "terra_originalmente_uniao": 8,"trecho_terreno_marginal":8, "trecho_terreno_marginal":8,"trecho_area_indubitavel":8, "terras_interiores":8, "faixa_dominio":9, "area_especial":10}
        sql = 'select count(*) from ' + schemaName + '.' + tableName + ';'
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        lineNumber = 0
        for row in rows:
            lineNumber = row[0]

        sql = "select id_codigo from dominio.sigla_uf where nome_valor = '" + siglaUf + "'"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        siglaUfId = 0
        for row in rows:
            siglaUfId = row[0]

        idclasse = codeClassDic[tableName]

        print (siglaUfId * 100000000)
        print (idclasse * 1000000)

        newid = siglaUfId * 100000000 + idclasse * 1000000 + lineNumber + 1
        return newid

    #def getDadosAreaPoliticoAdministrativa(self, areaAdmin):







    #def setFeicao(self, tableName, newAtributesList):

    #def insertFeicao(self, tablename,atrbutesList):
