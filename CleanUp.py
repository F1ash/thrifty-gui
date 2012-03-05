# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, stat, os.path

class CleanUp(QWidget):
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
		''' запустить поток и по сигналу включить закладки '''
		QTimer.singleShot(5000, self.qwerty)

	def setState(self, state):
		self.dirList.setEnabled(state)
		self.addPath.setEnabled(state)
		self.delPath.setEnabled(state)
		self.editTargets.setEnabled(state)
		self.start.setEnabled(state)

	def qwerty(self):
		self.runned = False
		self.pid = -1
		self.Parent.setTabsState(True)
		self.progress.hide()
		pathToLog = '/tmp/11111'  ## TODO : detect Log file name
		self.logIn.setText('<a href="%s">Log in $TEMP<a>' % pathToLog)

	def editTargetsFile(self): pass
