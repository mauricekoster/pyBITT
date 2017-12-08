#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import ConfigParser
from PyQt4.QtGui import QMainWindow, QFont, QPushButton, QToolTip, QIcon, QWidget, QListWidget, QHBoxLayout, QPixmap
from PyQt4.QtGui import QLabel

from PyQt4 import QtGui, QtCore

icon_theme_config = None
#icon_theme_base_dir = '/usr/share/icons'
icon_theme_name = 'oxygen'

icon_theme_base_dir = os.path.join(os.path.expanduser('~'), '.icons')
#icon_theme_name = 'Winux10'
icons_dirs_list = []

def qicon_from_theme(name):
    global icon_theme_config, icons_dirs_list
    if icon_theme_config is None:
        icon_theme_config = ConfigParser.ConfigParser()

        icon_theme_config.read(os.path.join(icon_theme_base_dir, icon_theme_name, 'index.theme'))

        dirs = icon_theme_config.get('Icon Theme', 'Directories')
        icons_dirs_list = dirs.split(',')
        icons_dirs_list.reverse()

    found = False
    for d in icons_dirs_list:
        for ext in ['svg', 'png', 'xpm']:
            fn = os.path.join(icon_theme_base_dir, icon_theme_name, d, "%s.%s" % (name, ext))
            if os.path.exists(fn):
                found = True
                break
        if found:
            break

    if not found:
        # Fallback
        fn = 'icons/%s.svg' % name
        if not os.path.exists(fn):
            fn = 'icons/%s.png' % name

    print("icon '%s': %s" % (name, fn))
    return QIcon(fn)



class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

        self.selected_dir = None
        self.selected_theme = None
        self.selected_sub_dir = None

    def initUI(self):
        self.resize(1000, 500)
        self.center()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('accept.png'))

        w = self.create_central_widget()
        self.setCentralWidget(w)
        #self.setLayout(w)

        # status bar
        self.statusBar().showMessage('Ready')

        # Actions
        self.create_actions()

        # Menu
        self.create_menus()

        # Toolbar
        self.create_toolbars()

    # def create_central_widget(self):
    #     return QtGui.QTextEdit()
    def select_icon(self, item):
        icon = str(item.text())
        p = os.path.join(self.selected_dir, self.selected_theme, self.selected_sub_dir, icon)

        pixmap = QPixmap(p)
        self.image.setPixmap(pixmap)
        self.image.resize(pixmap.width(), pixmap.height())

    def select_sub_dir(self, item):
        subdir = str(item.text())
        self.selected_sub_dir = subdir

        p = os.path.join(self.selected_dir, self.selected_theme, subdir)

        d = [x for x in os.listdir(p)]
        print(d)
        d = [x for x in d if os.path.isfile(os.path.join(p, x))]
        print(d)
        d.sort()

        self.icon_list.clear()
        self.icon_list.addItems(d)

    def select_theme(self, item):
        p = str(item.text())
        self.selected_theme = p
        icon_theme_config = ConfigParser.ConfigParser()

        icon_theme_config.read(os.path.join(self.selected_dir, p, 'index.theme'))

        dirs = icon_theme_config.get('Icon Theme', 'Directories')
        icons_dirs_list = dirs.split(',')
        self.sub_dir_list.clear()
        self.sub_dir_list.addItems(icons_dirs_list)

    def select_dir(self, item):
        p = str(item.text())

        self.theme_list.clear()
        if os.path.exists(p):
            self.selected_dir = p

            d = [x for x in os.listdir(p)]
            print(d)
            d = [x for x in d if os.path.isdir(os.path.join(p, x))]
            print(d)
            d = [x for x in d if os.path.exists(os.path.join(p, x, 'index.theme'))]
            self.theme_list.addItems(d)

    def create_central_widget(self):
        widget = QWidget()
        vbox = QHBoxLayout()
        # widget.setLayout(grid)
        my_dir_list = QListWidget()
        my_dir_list.itemClicked.connect(self.select_dir)
        my_dir_list.addItem(os.path.join(os.environ['HOME'], '.icons'))
        my_dir_list.addItems([os.path.join(x, 'icons') for x in get_xdr_data_dirs()])
        my_dir_list.addItem('/usr/share/pixmaps')
        vbox.addWidget(my_dir_list)

        self.theme_list = QListWidget()
        self.theme_list.itemClicked.connect(self.select_theme)
        vbox.addWidget(self.theme_list)

        self.sub_dir_list = QListWidget()
        self.sub_dir_list.itemClicked.connect(self.select_sub_dir)
        vbox.addWidget(self.sub_dir_list)

        self.icon_list = QListWidget()
        self.icon_list.itemClicked.connect(self.select_icon)
        vbox.addWidget(self.icon_list)

        self.image = QLabel()
        self.image.setFixedWidth(150)
        vbox.addWidget(self.image)

        widget.setLayout(vbox)
        return widget

    def create_actions(self):
        self.exitAction = QtGui.QAction(qicon_from_theme('application-exit'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        # self.exitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.exitAction.triggered.connect(self.close)

    def create_toolbars(self):
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exitAction)

    def create_menus(self):
        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

    # def closeEvent(self, event):
    #
    #     reply = QtGui.QMessageBox.question(self, 'Message',
    #                                        "Are you sure to quit?", QtGui.QMessageBox.Yes |
    #                                        QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    #
    #     if reply == QtGui.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QtGui.QApplication(sys.argv)

    w = Example()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
