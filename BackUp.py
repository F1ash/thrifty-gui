# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os.path

SPEED = {
		'Slow'		: 2,
		'Normal'	: 1,
		'Fast'		: 0,
		'Fast+'		: 3
		}

USER_DESCRIPTION = \
'<pre><font color=green><b>UserMode</b></font> backs up own $HOME only\
<pre>\twithout Excludes path.'
ROOT_DESCRIPTION = \
'<pre><font color=red><b>RootMode</b></font> backs up catalogs:\
<pre>\t/usr/local\
<pre>\t/var/named/chroot\
<pre>\t/etc\
<pre>\t&lt;all real $HOMEs in system&gt;\
<pre>\twithout Excludes path.\
'

class BackUp(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent
		self.runned = False

		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignLeft)

		self.buttonLayout = QVBoxLayout()
		self.buttonLayout.setAlignment(Qt.AlignCenter)
		self.mode = QComboBox()
		self.mode.setIconSize(QSize(32,32))
		self.mode.setToolTip('Mode of task')
		self.mode.addItems(QStringList() << 'User' << 'Root')
		self.mode.setItemIcon (0, QIcon('/usr/share/thrifty/icons/user.png'))
		self.mode.setItemIcon (1, QIcon('/usr/share/thrifty/icons/admin.png'))
		self.speed = QComboBox()
		self.speed.setIconSize(QSize(32,32))
		self.speed.addItems(QStringList() << 'Slow' << 'Normal' << 'Fast' << 'Fast+')
		self.speed.setItemIcon (0, QIcon('/usr/share/thrifty/icons/slow.png'))
		self.speed.setItemIcon (1, QIcon('/usr/share/thrifty/icons/normal.png'))
		self.speed.setItemIcon (2, QIcon('/usr/share/thrifty/icons/fast.png'))
		self.speed.setItemIcon (3, QIcon('/usr/share/thrifty/icons/fast+.png'))
		self.speed.setToolTip('Speed of task execution')
		self.editExcludes = QPushButton(QIcon('/usr/share/thrifty/icons/edit.png'), '')
		self.editExcludes.setIconSize(QSize(32,32))
		self.editExcludes.setToolTip('Edit Excludes file for current regime')
		self.editExcludes.clicked.connect(self.editExcludesFile)
		self.start = QPushButton(QIcon('/usr/share/thrifty/icons/start.png'), '')
		self.start.setIconSize(QSize(32,32))
		self.start.clicked.connect(self.runBackUp)
		self.start.setToolTip('Start task')

		self.buttonLayout.addWidget(self.mode)
		self.buttonLayout.addWidget(self.speed)
		self.buttonLayout.addWidget(self.editExcludes)
		self.buttonLayout.addWidget(self.start)

		self.descriptionTask = QLabel(USER_DESCRIPTION)
		self.descriptionTask.setAlignment(Qt.AlignLeft)

		self.progress = QProgressBar()
		self.progress.setOrientation(Qt.Vertical)
		self.progress.hide()
		self.progress.setRange(0, 0)

		self.logIn = QLabel('')
		self.logIn.setToolTip('Log of processed task')
		self.logIn.setOpenExternalLinks(True)

		self.layout.addItem(self.buttonLayout, 0, 0)
		self.layout.addWidget(self.progress, 0, 1)
		self.layout.addWidget(self.descriptionTask, 0, 2)
		self.layout.addWidget(self.logIn, 1, 0)

		self.setLayout(self.layout)
		self.mode.currentIndexChanged.connect(self.changeContent)

	def changeContent(self, i = 0):
		if i :
			self.descriptionTask.setText(ROOT_DESCRIPTION)
			self.editExcludes.setToolTip('Edit Excludes file for <font color=red><b>ROOT</b></font> mode')
		else :
			self.descriptionTask.setText(USER_DESCRIPTION)
			self.editExcludes.setToolTip('Edit Excludes file for <font color=green><b>USER</b></font> mode')

	def runBackUp(self):
		self.Parent.setTabsState(False)
		self.progress.show()
		self.runned = True
		mode = 0 if self.mode.currentIndex() else 1
		speed = SPEED[str(self.speed.currentText())]
		print 'BackUp running in %i mode and %i speed ...' % (mode, speed)
		self.t = QProcess()
		Data = QStringList()
		Data.append('/usr/share/thrifty/thrifty.py')
		Data.append('G:' + str(speed))
		self.t.finished.connect(self.showResult)
		if mode : self.t.start('python', Data)
		else : self.t.start('pkexec', Data)
		if self.t.waitForStarted() :
			self.runned = True
			print self.t.state()
		else :
			self.showResult()

	def setState(self, state):
		self.mode.setEnabled(state)
		self.speed.setEnabled(state)
		self.editExcludes.setEnabled(state)
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
		else :
			pathToLog = 'ERROR'
		self.logIn.setText('<a href="%s">Log in $TEMP<a>' % pathToLog)

	def editExcludesFile(self): pass
