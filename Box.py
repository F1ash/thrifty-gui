# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from CheckFile import CheckFile
from BackUp import BackUp
from CleanUp import CleanUp

class Box(QTabWidget):
	def __init__(self, parent = None):
		QTabWidget.__init__(self, parent)
		self.Parent = parent

		self.setMovable(True)

		self.checkFile = CheckFile(self)
		self.backUp = BackUp(self)
		self.cleanUp = CleanUp(self)

		self.addTab(self.checkFile, QIcon(), QString('File'))
		self.setTabToolTip(0, 'Checks file belonging to a rpmdb')

		self.addTab(self.backUp, QIcon(), QString('BackUp'))
		self.setTabToolTip(1, 'Back up "rpmdb-out" files (User\Root Mode).')

		self.addTab(self.cleanUp, QIcon(), QString('Clean'))
		self.setTabToolTip(2, 'Clean up "rpmdb-out" files (Root Mode only) or test.')

	def setTabsState(self, state):
		self.checkFile.setState(state)
		self.backUp.setState(state)
		self.cleanUp.setState(state)
		self.Parent.stopProcess.setEnabled(not state)
