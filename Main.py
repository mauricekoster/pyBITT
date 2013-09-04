from PySide import QtCore, QtGui, QtWebKit
import os, sys

class Main(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout()
        self.editor = QtGui.QPlainTextEdit()
        self.preview = QtWebKit.QWebView()
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.preview)
        self.editor.textChanged.connect(self.updatePreview)
        self.setLayout(self.layout)

    def updatePreview(self):
        self.preview.setHtml(self.editor.toPlainText())

def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
