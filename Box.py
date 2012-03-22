# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from CheckFile import CheckFile
from BackUp import BackUp
from CleanUp import CleanUp
from BrokenSearch import Broken
from Translator import Translator

class Box(QTabWidget):
	def __init__(self, parent = None):
		QTabWidget.__init__(self, parent)
		self.Parent = parent
		self.tr = Translator('Thrifty')

		self.setMovable(True)
		self.setIconSize(QSize(32,32))

		self.checkFile = CheckFile(self)
		self.backUp = BackUp(self)
		self.cleanUp = CleanUp(self)
		self.broken = Broken(self)

		self.addTab(self.checkFile, QIcon('/usr/share/thrifty/icons/file.png'), QString(self.tr._translate('File')))
		self.setTabToolTip(0, self.tr._translate('Checks file belonging to a rpmdb'))

		self.addTab(self.backUp, QIcon('/usr/share/thrifty/icons/backup.png'), QString(self.tr._translate('BackUp')))
		self.setTabToolTip(1, self.tr._translate('Back up "rpmdb-out" files <b>(User\Root Mode)</b>.'))

		self.addTab(self.cleanUp, QIcon('/usr/share/thrifty/icons/cleanup.png'), QString(self.tr._translate('CleanUp')))
		self.setTabToolTip(2, self.tr._translate('Clean up "rpmdb-out" files <b>(Root Mode only)</b> or test.'))

		self.addTab(self.broken, QIcon('/usr/share/thrifty/icons/file.png'), QString(self.tr._translate('Broken')))
		self.setTabToolTip(3, self.tr._translate('Search broken packages <b>(Root Mode only)</b>.'))

	def setTabsState(self, state):
		self.checkFile.setState(state)
		self.backUp.setState(state)
		self.cleanUp.setState(state)
		self.broken.setState(state)
		self.Parent.stopProcess.setEnabled(not state)
