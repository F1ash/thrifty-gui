#!/usr/bin/python 
# -*- coding: utf-8 -*-

import os, sys, locale, time
from PyQt4 import QtGui, QtCore
from MainWindow import MainWindow

locale.setlocale(locale.LC_ALL, 'C')
app = QtGui.QApplication(sys.argv)
pixmap = QtGui.QPixmap ('/usr/share/thrifty/icons/warning.png')
splash = QtGui.QSplashScreen (pixmap, QtCore.Qt.WindowStaysOnTopHint)
splash.show()
app.processEvents()
main = MainWindow()
main.show()
for i in xrange(700) :
	splash.showMessage("", QtCore.Qt.AlignCenter, QtCore.Qt.yellow)
	app.processEvents()
splash.finish(main)
sys.exit(app.exec_())
