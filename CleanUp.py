# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Wait import Wait
import os, stat, os.path

class CleanUp(QWidget):
	stop = pyqtSignal()
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent
		self.runned = False
		self.pid = -1

		self.layout = QGridLayout()

		self.dirList = QListWidget()
		self.dirList.setMaximumHeight(150)
		self.dirList.setToolTip('A list of directories processed')

		self.buttonLayout = QVBoxLayout()
		self.addPath = QPushButton()
		self.delPath = QPushButton()
		self.editTargets = QPushButton()
		self.start = QPushButton()
		self.addPath.setToolTip('Add to List')
		self.delPath.setToolTip('Delete from List')
		self.editTargets.setToolTip('Edit Targets file for current regime')
		self.start.setToolTip('Start task')
		self.addPath.clicked.connect(self.addDirPath)
		self.delPath.clicked.connect(self.delDirPath)
		self.editTargets.clicked.connect(self.editTargetsFile)
		self.start.clicked.connect(self.runCleanUp)

		self.buttonLayout.addWidget(self.addPath)
		self.buttonLayout.addWidget(self.delPath)
		self.buttonLayout.addWidget(self.editTargets)
		self.buttonLayout.addWidget(self.start)

		self.progress = QProgressBar()
		self.progress.setOrientation(Qt.Vertical)
		self.progress.hide()
		self.progress.setRange(0, 0)

		self.logIn = QLabel('')
		self.logIn.setToolTip('Log of processed task')
		self.logIn.setOpenExternalLinks(True)

		self.layout.addWidget(self.dirList, 0, 0)
		self.layout.addItem(self.buttonLayout, 0, 1)
		self.layout.addWidget(self.progress, 0, 2)
		self.layout.addWidget(self.logIn, 1, 0)

		self.setLayout(self.layout)
		self.stop.connect(self.showResult)

	def addDirPath(self):
		_nameDir = QFileDialog.getExistingDirectory(self, 'Path_to_', '~', QFileDialog.ShowDirsOnly)
		nameDir = _nameDir.toLocal8Bit().data()
		if os.path.isdir(nameDir) and \
				os.access(nameDir, os.R_OK) and os.access(nameDir, os.X_OK) :
			self.dirList.addItem(_nameDir)
		else :
			msg = QMessageBox.information(self, 'ERROR', 'error', QMessageBox.Ok)

	def delDirPath(self):
		item = self.dirList.takeItem(self.dirList.currentRow())

	def runCleanUp(self):
		self.Parent.setTabsState(False)
		self.progress.show()
		self.runned = True
		print 'ClenUp running  ...'
		t = QProcess()
		Data = QStringList()
		#Data.append('/usr/bin/python')
		Data.append('./thrifty.py')
		Data.append('G:-t')
		for i in xrange(self.dirList.count()) :
			item_ = self.dirList.item(i)
			Data.append(item_.text())
		self.runned, self.pid = t.startDetached ('/usr/bin/pkexec', Data, os.path.expanduser('~/thrifty') ) #os.getcwd())
		print [self.runned, self.pid]
		if self.runned :
			self.waitProcess = Wait(self.pid, self)
			self.waitProcess.start()
		else :
			self.showResult()

	def setState(self, state):
		self.dirList.setEnabled(state)
		self.addPath.setEnabled(state)
		self.delPath.setEnabled(state)
		self.editTargets.setEnabled(state)
		self.start.setEnabled(state)

	def showResult(self):
		self.runned = False
		self.pid = -1
		self.Parent.setTabsState(True)
		self.progress.hide()
		name_ = '/dev/shm/thrifty.lastTask'
		if os.path.isfile(name_) :
			with open(name_, 'rb') as f :
				pathToLog = f.read()
			os.remove(name_)
		else :
			pathToLog = 'ERROR'
		self.logIn.setText('<a href="%s">Log in $TEMP<a>' % pathToLog)

	def editTargetsFile(self): pass
