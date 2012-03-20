# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Functions import USER_UID, USER_GID
import os, stat, os.path

def wrapData(args):
	return \
	'<pre>RealData : PackageData\
	<pre>Size: %s : %s<pre>Mode: %s : %s<pre>User: %s : %s<pre>Group: %s : %s<pre>Mtime: %s : %s' \
	% (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9]) + \
	('<pre>Link:\t%s<pre>\t%s' % (args[10], args[11]) if (args[10], args[11])!=('', '') else '') + \
	('<pre>WARNING: not unique data in rpmDB (%s records)' % args[12] if int(args[12])>1 else '')

class CheckFile(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent
		self.runned = False

		self.layout = QGridLayout()

		self.pathLayout = QHBoxLayout()

		self.pathString = QLineEdit('')
		self.pathString.returnPressed.connect(self.checkFile)
		self.searchPath = QPushButton(QIcon('/usr/share/thrifty/icons/file.png'), '')
		self.searchPath.setIconSize(QSize(32,32))
		self.searchPath.setToolTip('Path to file')
		self.searchPath.clicked.connect(self.addPath)

		self.pathLayout.addWidget(self.pathString)
		self.pathLayout.addWidget(self.searchPath)

		self.layout.addItem(self.pathLayout, 0, 0, 2, 3)

		self.package = QLabel('Package :')

		self.mode = QComboBox()
		self.mode.setIconSize(QSize(32,32))
		self.mode.addItem (QIcon('/usr/share/thrifty/icons/user.png'), '')
		self.mode.addItem (QIcon('/usr/share/thrifty/icons/admin.png'), '')
		self.mode.setToolTip('User Mode')
		self.start = QPushButton(QIcon('/usr/share/thrifty/icons/start.png'), '')
		self.start.setIconSize(QSize(32,32))
		self.start.clicked.connect(self.checkFile)
		self.start.setToolTip('Start task')

		self.packageCheckSumm = QLabel('Package CheckSumm :')
		self.checkSumm = QLabel('Real CheckSumm :')
		self.packageRes = QLabel('')
		self.packageCheckSummRes = QLabel('')
		self.checkSummRes = QLabel('')
		self.otherData = QLabel('')
		self.layout.addWidget(self.package, 3, 0)
		self.layout.addWidget(self.mode, 4, 0, Qt.AlignLeft)
		self.layout.addWidget(self.start, 4, 0, Qt.AlignRight)
		self.layout.addWidget(self.packageCheckSumm, 5, 0)
		self.layout.addWidget(self.checkSumm, 6, 0)
		self.layout.addWidget(self.packageRes, 3, 1)
		self.layout.addWidget(self.otherData, 4, 1)
		self.layout.addWidget(self.packageCheckSummRes, 5, 1)
		self.layout.addWidget(self.checkSummRes, 6, 1)

		self.setLayout(self.layout)
		self.mode.currentIndexChanged.connect(self.changeMode)
		self.setMinimumSize(32, 32)

	def changeMode(self, i = 0):
		if i :
			self.mode.setToolTip('Root Mode')
		else :
			self.mode.setToolTip('User Mode')

	def addPath(self):
		fileName = QFileDialog.getOpenFileName(self, 'Path_to_', '~')
		name_ = fileName.toLocal8Bit().data()
		if os.path.lexists(name_) : #and \
			#	not stat.S_ISLNK(os.lstat(name_).st_mode) and os.access(name_, os.R_OK) :
			self.pathString.setText(fileName)
			self.pathString.setFocus()
		else :
			msg = QMessageBox.information(self, 'ERROR', 'error', QMessageBox.Ok)

	def checkFile(self):
		self.Parent.setTabsState(False)
		self.runned = True
		self.packageRes.setText('')
		self.packageCheckSummRes.setText('')
		self.checkSummRes.setText('')
		self.otherData.setText('')
		mode = 0 if self.mode.currentIndex() else 1
		path = self.pathString.text().toUtf8().data()
		if not os.access(path, os.R_OK) and mode == 1:
			with open('/dev/shm/thrifty.lastTask', 'wb') as f :
				f.write('package:Permissin denied.\nmulti:0')
			self.showResult()
			return
		self.t = QProcess()
		Data = QStringList()
		Data.append('/usr/share/thrifty/thrifty.py')
		opt = ''.join(('G:', str(USER_UID), '/', str(USER_GID), '::', '-f'))
		Data.append(opt)
		Data.append(self.pathString.text())
		self.t.finished.connect(self.showResult)
		if mode : self.t.start('python', Data)
		else : self.t.start('pkexec', Data)
		if self.t.waitForStarted() :
			self.runned = True
			#print self.t.state()
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
		self.Parent.setTabsState(True)
		name_ = '/dev/shm/thrifty.lastTask'
		if os.path.isfile(name_) :
			with open(name_, 'rb') as f :
				_data = f.read()
			os.remove(name_)
			data = _data.split('\n')
			STR = ['' for i in xrange(13)]
			for item in data :
				_data = item.split(':')
				if len(_data) > 1 :
					if _data[0] == 'package' :
						self.packageRes.setText(_data[1])
					elif _data[0] == 'sizeR' :
						STR[0] = _data[1]
					elif _data[0] == 'sizeP' :
						STR[1] = _data[1]
					elif _data[0] == 'hashR' :
						self.checkSummRes.setText(_data[1])
					elif _data[0] == 'hashP' :
						self.packageCheckSummRes.setText(_data[1])
					elif _data[0] == 'modeR' :
						STR[2] = _data[1]
					elif _data[0] == 'modeP' :
						STR[3] = _data[1]
					elif _data[0] == 'uidR' :
						STR[4] = _data[1]
					elif _data[0] == 'uidP' :
						STR[5] = _data[1]
					elif _data[0] == 'gidR' :
						STR[6] = _data[1]
					elif _data[0] == 'gidP' :
						STR[7] = _data[1]
					elif _data[0] == 'mtimeR' :
						STR[8] = _data[1]
					elif _data[0] == 'mtimeP' :
						STR[9] = _data[1]
					elif _data[0] == 'linkR' :
						STR[10] = _data[1]
					elif _data[0] == 'linkP' :
						STR[11] = _data[1]
					elif _data[0] == 'multi' :
						STR[12] = _data[1]
			self.otherData.setText(wrapData(STR))
		else :
			self.packageRes.setText('Error : not successfull.')
