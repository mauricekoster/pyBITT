from PySide import QtSql

class Configuration(object):
   

    def checkConfigTable(self):
        if "config" in self.db.tables():
            return

        sql = QtSql.QSqlQuery(self.db)
        sql.exec_("CREATE TABLE config (KEY VARCHAR2(50), VALUE VARCHAR2(1000))")

    def __init__(self, db):
        self.db = db
        self.__conf = {}

        self.checkConfigTable()

        self.sql_select = QtSql.QSqlQuery(self.db)
        self.sql_select.prepare("SELECT VALUE FROM config WHERE KEY=:key")

        self.sql_update = QtSql.QSqlQuery(self.db)
        self.sql_update.prepare("UPDATE config SET VALUE=:value WHERE KEY=:key")

        self.sql_insert = QtSql.QSqlQuery(self.db)
        self.sql_insert.prepare("INSERT INTO config (KEY, VALUE) VALUES (:key, :value)")

    def getItem(self, key):
        self.sql_select.bindValue(":key", key)
        self.sql_select.exec_()
        if self.sql_select.next():
            return self.sql_select.value(0)
        
        return None

    def setItem(self, key, value):
        self.sql_update.bindValue(":key", key)
        self.sql_update.bindValue(":value", value)
        self.sql_update.exec_()

        if self.sql_update.numRowsAffected() == 0:
            self.sql_insert.bindValue(":key", key)
            self.sql_insert.bindValue(":value", value)
            self.sql_insert.exec_()
