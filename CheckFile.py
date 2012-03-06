# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Wait import Wait
import os, stat, os.path

class CheckFile(QWidget):
	stop = pyqtSignal()
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent
		self.runned = False
		self.pid = -1

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
		self.packageRes = QLabel('')
		self.packageCheckSummRes = QLabel('')
		self.checkSummRes = QLabel('')
		self.layout.addWidget(self.package, 3, 0)
		self.layout.addWidget(self.packageCheckSumm, 4, 0)
		self.layout.addWidget(self.checkSumm, 5, 0)
		self.layout.addWidget(self.packageRes, 3, 1)
		self.layout.addWidget(self.packageCheckSummRes, 4, 1)
		self.layout.addWidget(self.checkSummRes, 5, 1)

		self.setLayout(self.layout)
		self.stop.connect(self.showResult)

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
		self.runned = True
		print self.pathString.text().toUtf8().data()
		t = QProcess()
		Data = QStringList()
		Data.append('./thrifty.py')
		Data.append('G:-f')
		Data.append(self.pathString.text())
		self.runned, self.pid = t.startDetached ('python', Data, os.path.expanduser('~/thrifty') ) #os.getcwd())
		print [self.runned, self.pid]
		if self.runned :
			self.waitProcess = Wait(self.pid, self)
			self.waitProcess.start()
		else :
			self.showResult()

	def setState(self, state):
		self.pathString.setEnabled(state)
		self.searchPath.setEnabled(state)
		self.package.setEnabled(state)
		self.packageCheckSumm.setEnabled(state)
		self.checkSumm.setEnabled(state)

	def showResult(self):
		self.runned = False
		self.pid = -1
		self.Parent.setTabsState(True)
		name_ = '/dev/shm/thrifty.lastTask'
		if os.path.isfile(name_) :
			with open(name_, 'rb') as f :
				_data = f.read()
			os.remove(name_)
			data = _data.split('\n')
			self.packageRes.setText(data[0])
			self.packageCheckSummRes.setText(data[1])
			self.checkSummRes.setText(data[2])
		else :
			self.packageRes.setText('Error : not successfull.')
			self.packageCheckSummRes.setText('--')
			self.checkSummRes.setText('--')
