from PyQt4 import QtCore, QtGui, QtWebKit, uic
import os, sys
from Project import Project

class MainApp(QtCore.QObject):
    def __init__(self):
        super(MainApp,self).__init__()
        self.ui = None
        self.resourcedir = "resources"

        self.__parse_command_line()
        self.__init_widgets()

    def show(self):
        if self.ui:
            self.ui.show()
            self.ui.raise_()

    def __parse_command_line(self):
        i = 0
        while i < len(sys.argv):
            if sys.argv[i] == "-resourcedir":
                self.resourcedir = sys.argv[i+1]
                i = i + 1
            i = i + 1

    def __resource(self, filename):
        if self.resourcedir != "":
            return os.path.join(self.resourcedir, filename)
        return filename

    def __init_widgets(self):

        # Load the UI from a Qt designer file.

        file = QtCore.QFile(self.__resource("main_window.ui"))
        file.open(QtCore.QFile.ReadOnly)
        self.ui = uic.loadUi(file, None)
        file.close()

        action = self.ui.findChild(QtGui.QAction,"actionOpen_project")
        action.triggered.connect(self.openFile)

    def openFile(self):
        # Use the stock Qt dialog to look for VTK files.
        filename, _ = QtGui.QFileDialog.getOpenFileName(self.ui, 'Open file', os.curdir, "*.project")

        if filename != "":
            self.project_filename = filename
            # Do something with the new database
            self.project = Project(self.project_filename)


# Create and show our custom window.
app = QtGui.QApplication(sys.argv)
main = MainApp()
main.show()
sys.exit(app.exec_())
