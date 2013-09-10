from PySide import QtSql

from Configuration import Configuration

class Project(object):
    
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

        self.__conf = Configuration(self.db)
        return self.__conf

    def getDataSourceNames(self):
        n = self.getConfiguration().getItem("datasources")
        if n:
            return n.split(",")
        else:
            return []

def getProject(filename):
    return Project(filename)


if __name__ == "__main__":
    import sys
    from PySide import QtGui

    app = QtGui.QApplication(sys.argv)
    prj = getProject("test.project")
    print prj.getName()
    cnf = prj.getConfiguration()
    cnf.setItem("test", 123)
    print cnf.getItem("test")
