# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from StatusBar import StatusBar
from ListingText import ListingText
from Box import Box
import os

## TODO : import from thrifty.py
HELP = \
	'Description:\n\
	Utility for archiving or cleaning "rpmdb-out" files.\n\
	\n\
	thrifty [option]\n\
		0	-	very fast, ~200MB memory\n\
		1	-	fast, ~150MB memory\n\
		2	-	very slow, ~100MB memory\n\
		3	-	super fast, ~200MB !\n\
			This action backs up "rpmdb-out" or brocken (file in rpmdb,\n\
			but checksum mismatched) files from own HOME only (user mode)\n\
			or /etc, /var/named/chroot, /usr/local, <all real HOME> (root mode).\n\
			Excludes specified in\n\
				/etc/thrifty.excludes (common)\n\
				~/.config/thrifty/thrifty.excludes (for HOME only)\n\
		-c (--clean) [dir0 dir1 .. dirN]\n\
			-	delete all (NOTE THIS!) "rpmdb-out" files from [dir0 dir1 .. dirN]\n\
			This means that you can remove a lot of icons, settings, etc files.\n\
			It`s a hard way (root mode only).\n\
			Targets specified in\n\
				/etc/thrifty.targets\n\
			If specified then the utility will be delete "rpmdb-out" files which contain\n\
			in path "target" string only, else -- delete all "rpmdb-out" files.\n\
		-t (--test) [dir0 dir1 .. dirN]\n\
			-	like --clean , but without removing files.\n\
			This action can be used to obtain the list of all "rpmdb-out" files.\n\
			And after editing it can be recorded in the /etc/thrifty.targets\n\
			for precise removal of files.\n\
		-f (--file) file\n\
			-	check the file (abspath) provided by some package and brocken\n\
		-h (--help)\n\
			-	help\n\
	'

class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)

		#self.resize(450, 350)
		self.setWindowTitle('Thrifty')
		self.setWindowIcon(QIcon('./icons/thrifty.png'))

		self.exit_ = QAction(QIcon('./icons/exit.png'), '&Exit', self)
		self.exit_.setShortcut('Ctrl+Q')
		self.exit_.setStatusTip('Exit application')
		self.connect(self.exit_, SIGNAL('triggered()'), self._close)

		listHelp = QAction(QIcon('./icons/help.png'),'&About Thrifty', self)
		listHelp.setStatusTip('Read help')
		self.connect(listHelp, SIGNAL('triggered()'), self.showMSG)

		self.stopProcess = QAction(QIcon('./icons/help.png'),'&Terminate Task', self)
		self.stopProcess.setShortcut('Ctrl+T')
		self.stopProcess.setStatusTip('Terminate running task ...')
		self.stopProcess.setEnabled(False)
		self.connect(self.stopProcess, SIGNAL('triggered()'), self.terminateRunningTask)

		self.statusBar = StatusBar(self)
		self.setStatusBar(self.statusBar)

		menubar = self.menuBar()

		file_ = menubar.addMenu('&File')
		file_.addAction(self.exit_)

		set_ = menubar.addMenu('&Control')
		set_.addAction(self.stopProcess)

		help_ = menubar.addMenu('&Help')
		help_.addAction(listHelp)

		self.menuTab = Box(self)
		self.setCentralWidget(self.menuTab)

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
		return name, obj

	def terminateRunningTask(self):
		name, obj = self.detectRunningTask()
		print 'Terminated Task : %s' % name
		obj.t.terminate()

	def showMSG(self):
		msg = ListingText(HELP, self)
		msg.exec_()

	def _close(self): self.close()
