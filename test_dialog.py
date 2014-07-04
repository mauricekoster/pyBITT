import sys
from PyQt4 import QtCore, QtGui, uic

class MyForm(QtCore.QObject):
    def __init__(self, dialog_filename="dialog.ui", parent=None):
        super(MyForm,self).__init__()

        print "fn: %s" % dialog_filename
        file = QtCore.QFile(dialog_filename)
        file.open(QtCore.QFile.ReadOnly)
        self.ui = uic.loadUi(file, None)
        file.close()

    def show(self):
        if self.ui:
            self.ui.show()
            self.ui.raise_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if len(sys.argv) > 1:
        myapp = MyForm( sys.argv[1] )
    else:
        myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
