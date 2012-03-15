# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from StatusBar import StatusBar
from ListingText import ListingText
from Box import Box
from thrifty import HELP
import os

class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)

		#self.resize(450, 350)
		self.setWindowTitle('Thrifty')
		self.setWindowIcon(QIcon('/usr/share/thrifty/icons/sniper_soldier.png'))

		self.Settings = QSettings('thrifty', 'thrifty')

		self.exit_ = QAction(QIcon('/usr/share/thrifty/icons/exit.png'), '&Exit', self)
		self.exit_.setShortcut('Ctrl+Q')
		self.exit_.setStatusTip('Exit application')
		self.connect(self.exit_, SIGNAL('triggered()'), self._close)

		listHelp = QAction(QIcon('/usr/share/thrifty/icons/help.png'),'&About Thrifty', self)
		listHelp.setStatusTip('Read help')
		self.connect(listHelp, SIGNAL('triggered()'), self.showMSG)

		self.stopProcess = QAction(QIcon('/usr/share/thrifty/icons/terminate.png'),'&Terminate Task', self)
		self.stopProcess.setShortcut('Ctrl+T')
		self.stopProcess.setStatusTip('Terminate running task ...')
		self.stopProcess.setEnabled(False)
		self.connect(self.stopProcess, SIGNAL('triggered()'), self.terminateRunningTask)

		self.separator = QAction('', self)
		self.separator.setSeparator(True)

		self.checkMode = QAction('check file`s &mode', self)
		self.checkMode.setCheckable(True)
		value = str(self.Settings.value('checkFileMode', 'False').toString())
		if value.lower() == 'true' :
			self.checkMode.setChecked(True)
		else :
			self.checkMode.setChecked(False)
		self.connect(self.checkMode, SIGNAL('changed()'), self.setCheckMode)

		self.checkOwners = QAction('check  file`s &owners', self)
		self.checkOwners.setCheckable(True)
		value = str(self.Settings.value('checkFileOwners', 'False').toString())
		if value.lower() == 'true' :
			self.checkOwners.setChecked(True)
		else :
			self.checkOwners.setChecked(False)
		self.connect(self.checkOwners, SIGNAL('changed()'), self.setCheckOwners)

		self.statusBar = StatusBar(self)
		self.setStatusBar(self.statusBar)

		menubar = self.menuBar()

		file_ = menubar.addMenu('&File')
		file_.addAction(self.exit_)

		set_ = menubar.addMenu('&Control')
		set_.addAction(self.stopProcess)
		set_.addAction(self.separator)
		set_.addAction(self.checkMode)
		set_.addAction(self.checkOwners)

		help_ = menubar.addMenu('&Help')
		help_.addAction(listHelp)

		self.menuTab = Box(self)
		self.setCentralWidget(self.menuTab)

	def setCheckMode(self):
		state = self.checkMode.isChecked()
		print state
		self.Settings.setValue('checkFileMode', state)

	def setCheckOwners(self):
		state = self.checkOwners.isChecked()
		#print state
		self.Settings.setValue('checkFileOwners', state)

	def detectRunningTask(self):
		name = 'Unknown'
		if self.menuTab.checkFile.runned :
			name = 'CheckFile'
			obj = self.menuTab.checkFile
		elif self.menuTab.backUp.runned :
			name = 'BackUp'
			obj = self.menuTab.backUp
		elif self.menuTab.cleanUp.runned :
			name = 'CleanUp'
			obj = self.menuTab.cleanUp
		elif self.menuTab.broken.runned :
			name = 'Search Broken'
			obj = self.menuTab.broken
		return name, obj

	def terminateRunningTask(self):
		name, obj = self.detectRunningTask()
		#print 'Terminated Task : %s' % name
		obj.t.terminate()

	def showMSG(self, s = ''):
		msg = ListingText(HELP if s=='' else s, self)
		msg.exec_()

	def _close(self):
		self.Settings.sync()
		self.close()
