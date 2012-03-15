# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Editor import Editor
from Functions import USER_UID, USER_GID
import os, os.path

class Broken(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent
		self.runned = False
		self.pathToLog = None

		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignCenter)

		self.dirList = QListWidget()
		#self.dirList.setMaximumHeight(150)
		self.dirList.setToolTip('A list of directories processed')

		self.buttonLayout = QVBoxLayout()
		self.buttonLayout.setAlignment(Qt.AlignCenter)
		self.addPath = QPushButton(QIcon('/usr/share/thrifty/icons/plus.png'), '')
		self.addPath.setIconSize(QSize(32,32))
		self.delPath = QPushButton(QIcon('/usr/share/thrifty/icons/delete.png'), '')
		self.delPath.setIconSize(QSize(32,32))
		self.showTargets = QPushButton(QIcon('/usr/share/thrifty/icons/show.png'), '')
		self.showTargets.setIconSize(QSize(32,32))
		self.mode = QComboBox()
		self.mode.setIconSize(QSize(32,32))
		self.mode.setToolTip('Packages')
		self.mode.addItem (QIcon('/usr/share/thrifty/icons/packages.png'), '')
		self.mode.addItem (QIcon('/usr/share/thrifty/icons/files.png'), '')
		self.start = QPushButton(QIcon('/usr/share/thrifty/icons/start.png'), '')
		self.start.setIconSize(QSize(32,32))
		self.addPath.setToolTip('Add to List')
		self.delPath.setToolTip('Delete from List')
		self.showTargets.setToolTip('show Targets file')
		self.start.setToolTip('Start task')
		self.addPath.clicked.connect(self.addDirPath)
		self.delPath.clicked.connect(self.delDirPath)
		self.showTargets.clicked.connect(self.showTargetsList)
		self.start.clicked.connect(self.runSearchBroken)

		self.buttonLayout.addWidget(self.addPath)
		self.buttonLayout.addWidget(self.delPath)
		self.buttonLayout.addWidget(self.start)
		self.buttonLayout.addWidget(self.mode)
		self.buttonLayout.addWidget(self.showTargets)

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
		self.mode.currentIndexChanged.connect(self.changeModeContent)

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

	def changeModeContent(self, i = 0):
		if i :
			self.mode.setToolTip('Files')
		else :
			self.mode.setToolTip('Packages')

	def runSearchBroken(self):
		self.Parent.setTabsState(False)
		self.progress.show()
		self.runned = True
		self.pathToLog = None
		print 'Search broken running  ...'
		self.t = QProcess()
		Data = QStringList()
		Data.append('--user')
		Data.append('root')
		Data.append('/usr/share/thrifty/thrifty.py')
		mode = '-b'
		value = str(self.Parent.Parent.Settings.value('checkFileOwners', 'False').toString())
		if value.lower() == 'true' :
			mode += 'O'
		value = str(self.Parent.Parent.Settings.value('checkFileMode', 'False').toString())
		if value.lower() == 'true' :
			mode += 'M'
		opt = ''.join(('G:', str(USER_UID), '/', str(USER_GID), '::', mode))
		Data.append(opt)
		for i in xrange(self.dirList.count()) :
			item_ = self.dirList.item(i)
			Data.append(item_.text())
		#for i in xrange(Data.count()) :
		#	print Data[i],
		self.t.finished.connect(self.showResult)
		self.t.start('pkexec', Data)
		if self.t.waitForStarted() :
			self.runned = True
			#print self.t.state()
		else :
			self.showResult()

	def setState(self, state):
		self.dirList.setEnabled(state)
		self.addPath.setEnabled(state)
		self.delPath.setEnabled(state)
		self.mode.setEnabled(state)
		self.showTargets.setEnabled(state)
		self.start.setEnabled(state)

	def showResult(self):
		self.runned = False
		self.Parent.setTabsState(True)
		self.progress.hide()
		name_ = '/dev/shm/thrifty.lastTask'
		if os.path.isfile(name_) :
			with open(name_, 'rb') as f :
				pathToLog = f.read()
			os.remove(name_)
			self.pathToLog = pathToLog
		else :
			pathToLog = 'ERROR'
		self.logIn.setText('<a href="%s">Log in $TEMP<a>' % pathToLog + '</a>')

	def showTargetsList(self):
		self.Parent.setTabsState(False)
		path_ = '' if self.pathToLog is None else self.pathToLog
		task = 0 if self.mode.currentIndex() else 1
		self.editor = Editor(path_, 0, self, task)
		self.editor.show()

	def enableEditorButton(self):
		self.Parent.setTabsState(True)
