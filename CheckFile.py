# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, stat, os.path

class CheckFile(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent
		
		self.layout = QGridLayout()

		self.pathLayout = QHBoxLayout()

		self.pathString = QLineEdit('')
		self.pathString.returnPressed.connect(self.checkFile)
		self.searchPath = QPushButton()
		self.searchPath.clicked.connect(self.addPath)

		self.pathLayout.addWidget(self.pathString)
		self.pathLayout.addWidget(self.searchPath)

		self.layout.addItem(self.pathLayout, 0, 0, 2, 3)

		self.package = QLabel('Package :')
		self.packageCheckSumm = QLabel('Package CheckSumm :')
		self.checkSumm = QLabel('Real CheckSumm :')
		self.layout.addWidget(self.package, 3, 0)
		self.layout.addWidget(self.packageCheckSumm, 4, 0)
		self.layout.addWidget(self.checkSumm, 5, 0)

		self.setLayout(self.layout)

	def addPath(self):
		fileName = QFileDialog.getOpenFileName(self, 'Path_to_', '~')
		name_ = fileName.toLocal8Bit().data()
		if os.path.isfile(name_) and \
				not stat.S_ISLNK(os.lstat(name_).st_mode) and os.access(name_, os.R_OK) :
			self.pathString.setText(fileName)
			self.pathString.setFocus()
		else :
			msg = QMessageBox.information(self, 'ERROR', 'error', QMessageBox.Ok)

	def checkFile(self):
		self.Parent.setTabsState(False)
		print self.pathString.text().toUtf8().data()
		''' запустить поток и по сигналу включить закладки '''
		QTimer.singleShot(5000, self.qwerty)

	def setState(self, state):
		self.pathString.setEnabled(state)
		self.searchPath.setEnabled(state)
		self.package.setEnabled(state)
		self.packageCheckSumm.setEnabled(state)
		self.checkSumm.setEnabled(state)

	def qwerty(self):
		self.Parent.setTabsState(True)
