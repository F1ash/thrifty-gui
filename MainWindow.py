# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from StatusBar import StatusBar
from ListingText import ListingText
from Box import Box
from thrifty import HELP
from Functions import prelinkInstalled
from Translator import Translator
import os

class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		self.runned = False
		self.tr = Translator('Thrifty')

		#self.resize(450, 350)
		self.setWindowTitle(self.tr._translate('Thrifty'))
		self.setWindowIcon(QIcon('/usr/share/thrifty/icons/sniper_soldier.png'))

		self.Settings = QSettings('thrifty', 'thrifty')

		self.exit_ = QAction(QIcon('/usr/share/thrifty/icons/exit.png'), self.tr._translate('&Exit'), self)
		self.exit_.setShortcut('Ctrl+Q')
		self.exit_.setStatusTip(self.tr._translate('Exit application'))
		self.connect(self.exit_, SIGNAL('triggered()'), self._close)

		listHelp = QAction(QIcon('/usr/share/thrifty/icons/help.png'), self.tr._translate('&About Thrifty'), self)
		listHelp.setStatusTip(self.tr._translate('Read help'))
		self.connect(listHelp, SIGNAL('triggered()'), self.showMSG)

		self.stopProcess = QAction(QIcon('/usr/share/thrifty/icons/terminate.png'), self.tr._translate('&Terminate Task'), self)
		self.stopProcess.setShortcut('Ctrl+T')
		self.stopProcess.setStatusTip(self.tr._translate('Terminate running task ...'))
		self.stopProcess.setEnabled(False)
		self.connect(self.stopProcess, SIGNAL('triggered()'), self.terminateRunningTask)

		self.separator = QAction('', self)
		self.separator.setSeparator(True)

		self.checkMode = QAction(self.tr._translate('check file`s &mode'), self)
		self.checkMode.setCheckable(True)
		value = str(self.Settings.value('checkFileMode', 'False').toString())
		if value.lower() == 'true' :
			self.checkMode.setChecked(True)
		else :
			self.checkMode.setChecked(False)
		self.connect(self.checkMode, SIGNAL('changed()'), self.setCheckMode)

		self.checkOwners = QAction(self.tr._translate('check  file`s &owners'), self)
		self.checkOwners.setCheckable(True)
		value = str(self.Settings.value('checkFileOwners', 'False').toString())
		if value.lower() == 'true' :
			self.checkOwners.setChecked(True)
		else :
			self.checkOwners.setChecked(False)
		self.connect(self.checkOwners, SIGNAL('changed()'), self.setCheckOwners)

		self.checkMtime = QAction(self.tr._translate('check  file`s mt&ime'), self)
		self.checkMtime.setCheckable(True)
		value = str(self.Settings.value('checkFileMtime', 'False').toString())
		if value.lower() == 'true' :
			self.checkMtime.setChecked(True)
		else :
			self.checkMtime.setChecked(False)
		self.connect(self.checkMtime, SIGNAL('changed()'), self.setCheckMtime)

		self.statusBar = StatusBar(self)
		self.setStatusBar(self.statusBar)

		self.prelink = QAction(QIcon('/usr/share/thrifty/icons/prelink.png'), self.tr._translate('&Prelink'), self)
		self.prelink.setShortcut('Ctrl+P')
		self.prelink.setStatusTip(self.tr._translate('Prelink now'))
		self.prelink.setEnabled(prelinkInstalled)
		self.connect(self.prelink, SIGNAL('triggered()'), self.runPrelink)

		menubar = self.menuBar()

		file_ = menubar.addMenu(self.tr._translate('&File'))
		file_.addAction(self.prelink)
		file_.addAction(self.exit_)

		set_ = menubar.addMenu(self.tr._translate('&Control'))
		set_.addAction(self.stopProcess)
		set_.addAction(self.separator)
		set_.addAction(self.checkMode)
		set_.addAction(self.checkOwners)
		set_.addAction(self.checkMtime)

		help_ = menubar.addMenu(self.tr._translate('&Help'))
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

	def setCheckMtime(self):
		state = self.checkMtime.isChecked()
		#print state
		self.Settings.setValue('checkFileMtime', state)

	def detectRunningTask(self):
		name = 'Unknown'
		obj = None
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
		elif self.runned :
			name = 'Prelink'
			obj = self
		return name, obj

	def terminateRunningTask(self):
		name, obj = self.detectRunningTask()
		#print 'Terminated Task : %s' % name
		if obj is not None : obj.t.terminate()

	def runPrelink(self):
		self.prelink.setEnabled(False)
		self.menuTab.setTabsState(False)
		#self.progress.show()
		self.runned = True
		print 'Prelink running  ...'
		self.t = QProcess()
		Data = QStringList()
		Data.append('prelink')
		Data.append('-a')
		self.t.finished.connect(self.showResult)
		self.t.start('pkexec', Data)
		if self.t.waitForStarted() :
			self.runned = True
			#print self.t.state()
		else :
			self.showResult()

	def showResult(self):
		self.prelink.setEnabled(True)
		self.runned = False
		self.menuTab.setTabsState(True)

	def showMSG(self, s = ''):
		msg = ListingText(HELP if s=='' else s, self)
		msg.exec_()

	def _close(self):
		self.Settings.sync()
		self.close()
