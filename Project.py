from PySide import QtSql

from Configuration import Configuration
from Datasources import Datasources

class MissingPKException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Project(object):



    registeredTables = {}

    def __init__(self, filename):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(filename)
        if not self.db.open():
            print "No connection!"
            self.db = None
        self.__conf = None

    def getName(self):
        return "No Name"


    def getConfiguration(self):
        if self.__conf:
            return self.__conf

        self.__conf = Configuration(self)
        return self.__conf

    def getDataSources(self):
        if self.__ds:
            return self.__ds

        self.__ds = Datasources(self)
        return self.__ds


    def registerTable(self, table):
        if table['name'] in self.registeredTables.keys():
            return

        # should the table be created? aka does the table already exists?
        if not table['name'] in self.db.tables():
            s = self._construct_create_statement( table )
            sql = QtSql.QSqlQuery(s, self.db)
            sql.exec_()

        self.registeredTables[ table['name'] ] = table


    def storeRecord(self, tablename, record):
        (pk, other) = self.__field_helper( self.registeredTables[ tablename ], record )

        # try update
        s = "UPDATE %s SET " % tablename
        s += ",".join([fld + " = :" + fld for fld in other ])
        s += " WHERE "
        s += ",".join([fld + " = :" + fld for fld in pk ])


        sql = QtSql.QSqlQuery(self.db)

        sql.prepare(s)
        for fld in record.keys():
            sql.bindValue(":"+fld, record[fld])

        sql.exec_()

        if sql.numRowsAffected() == 0:
            # try insert
            s = "INSERT INTO %s (" % tablename
            s += ",".join([fld for fld in record.keys() ])
            s += ") VALUES ("
            s += ",".join([":" + fld for fld in record.keys() ])
            s += ")"

            sql.prepare(s)
            for fld in record.keys():
                sql.bindValue(":"+fld, record[fld])

            sql.exec_()

    def getRecords(self, tablename, search):

        flds = [fld[0] for fld in self.registeredTables[ tablename ]['fields']]
        s = "SELECT "
        s += ",".join(flds)
        s += " FROM %s WHERE " % tablename
        s += ",".join([ fld + " = :" + fld for fld in search.keys() ])

        sql = QtSql.QSqlQuery(self.db)

        sql.prepare(s)
        for fld in search.keys():
            sql.bindValue(":"+fld, search[fld])

        sql.exec_()

        if sql.numRowsAffected() == 0:
            return []

        lst = []
        rec = sql.record()

        while sql.next():
            d = {}
            for fld in flds:
                c = rec.indexOf(fld)
                d[fld] = sql.value(c)

            lst.append(d)

        return lst

    def __field_helper(self, table, record):
        pk = [fld[0] for fld in  table['fields'] if len(fld)==4 and fld[3]]
        other = [fld for fld in record.keys() if not fld in pk]
        missingpk = [fld for fld in pk if not fld in record.keys()]

        if len(missingpk):
            raise MissingPKException("Missing PK values")

        if len(other)==0:
            raise MissingPKException("Missing other values")
 
        return (pk, other)

    def _construct_create_statement(self, table):
        nm = table['name']
        s = "CREATE TABLE %s (" % nm
        for fld in table['fields']:
            s += "%s %s" % (fld[0], fld[1])
            if len(fld) == 4:
                if fld[3]:
                    s += " PRIMARY KEY"

            s += "," 

        s = s[:-1] + ")"
        return s



def getProject(filename):
    return Project(filename)


