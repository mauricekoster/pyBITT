from PyQt4 import QtSql

class Configuration(object):


    def __init__(self, project):
        self.project = project
        self.__conf = {}

        self.project.registerTable( dict(
                name='config',
                fields=[
                        ('key','VARCHAR2(50)',True, True),
                        ('value','VARCHAR2(1000)')
                    ]
            ) )

    def getItem(self, key):
        lst = self.project.getRecords('config', { 'key': key } )
        print lst
        if lst:
            return lst[0]['value']
        else:
            return None

    def setItem(self, key, value):
        self.project.storeRecord('config', { 'key' : key, 'value': value } )
