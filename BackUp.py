# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Editor import Editor
from Translator import Translator
from Functions import USER_UID, USER_GID
import os.path

SPEED = {0	: 2, 1	: 1, 2	: 0, 3	: 3}

def USER_DESCRIPTION(chunk0, chunk1):
	return \
'<pre><font color=green><b>UserMode</b></font> ' + chunk0 + \
'<pre>\t' + chunk1

def ROOT_DESCRIPTION(chunk0, chunk1, chunk2):
	return \
'<pre><font color=red><b>RootMode</b></font> ' + chunk0 + \
'<pre>\t/usr/local\
<pre>\t/var/named/chroot\
<pre>\t/etc\
<pre>\t&lt;' + chunk1 + '&gt;\
<pre>\t' + chunk2

class BackUp(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent
		self.tr = Translator('Thrifty')
		self.runned = False
		self.trChunk0 = self.tr._translate('backs up own $HOME only')
		self.trChunk1 = self.tr._translate('without Excludes path.')
		self.trChunk2 = self.tr._translate('backs up catalogs:')
		self.trChunk3 = self.tr._translate('all real $HOMEs in system')

		self.layout = QGridLayout()
		self.layout.setAlignment(Qt.AlignLeft)

		self.buttonLayout = QVBoxLayout()
		self.buttonLayout.setAlignment(Qt.AlignCenter)
		self.mode = QComboBox()
		self.mode.setIconSize(QSize(32,32))
		#self.mode.addItems(QStringList() << 'User' << 'Root')
		self.mode.addItem (QIcon('/usr/share/thrifty/icons/user.png'), '')
		self.mode.addItem (QIcon('/usr/share/thrifty/icons/admin.png'), '')
		self.mode.setToolTip(self.tr._translate('User Mode'))
		self.speed = QComboBox()
		self.speed.setIconSize(QSize(32,32))
		#self.speed.addItems(QStringList() << 'Slow' << 'Normal' << 'Fast' << 'Fast+')
		self.speed.addItem (QIcon('/usr/share/thrifty/icons/slow.png'), '')
		self.speed.addItem (QIcon('/usr/share/thrifty/icons/normal.png'), '')
		self.speed.addItem (QIcon('/usr/share/thrifty/icons/fast.png'), '')
		self.speed.addItem (QIcon('/usr/share/thrifty/icons/fast+.png'), '')
		self.speed.setToolTip(self.tr._translate('Slow'))
		self.editExcludes = QPushButton(QIcon('/usr/share/thrifty/icons/edit.png'), '')
		self.editExcludes.setIconSize(QSize(32,32))
		self.editExcludes.setToolTip(self.tr._translate('Edit Excludes file for current regime'))
		self.editExcludes.clicked.connect(self.editExcludesFile)
		self.start = QPushButton(QIcon('/usr/share/thrifty/icons/start.png'), '')
		self.start.setIconSize(QSize(32,32))
		self.start.clicked.connect(self.runBackUp)
		self.start.setToolTip(self.tr._translate('Start task'))

		self.buttonLayout.addWidget(self.mode)
		self.buttonLayout.addWidget(self.speed)
		self.buttonLayout.addWidget(self.editExcludes)
		self.buttonLayout.addWidget(self.start)

		self.descriptionTask = QLabel('')
		self.descriptionTask.setAlignment(Qt.AlignLeft)

		self.progress = QProgressBar()
		self.progress.setOrientation(Qt.Vertical)
		self.progress.hide()
		self.progress.setRange(0, 0)

		self.logIn = QLabel('')
		self.logIn.setToolTip(self.tr._translate('Log of processed task'))
		self.logIn.setOpenExternalLinks(True)

		self.layout.addItem(self.buttonLayout, 0, 0)
		self.layout.addWidget(self.progress, 0, 1)
		self.layout.addWidget(self.descriptionTask, 0, 2)
		self.layout.addWidget(self.logIn, 1, 0)

		self.setLayout(self.layout)
		self.mode.currentIndexChanged.connect(self.changeModeContent)
		self.speed.currentIndexChanged.connect(self.changeSpeedContent)
		self.mode.currentIndexChanged.emit(0)

	def changeModeContent(self, i = 0):
		if i :
			self.mode.setToolTip(self.tr._translate('Root Mode'))
			self.descriptionTask.setText(ROOT_DESCRIPTION(self.trChunk2, self.trChunk3, self.trChunk1))
			self.editExcludes.setToolTip(self.tr._translate('Edit Excludes file for ') + \
					'<font color=red><b>ROOT</b></font> ' + \
					self.tr._translate('mode'))
		else :
			self.mode.setToolTip(self.tr._translate('User Mode'))
			self.descriptionTask.setText(USER_DESCRIPTION(self.trChunk0, self.trChunk1))
			self.editExcludes.setToolTip(self.tr._translate('Edit Excludes file for ') + \
					'<font color=green><b>USER</b></font> ' + \
					self.tr._translate('mode'))

	def changeSpeedContent(self, i = 0):
		if i == 3 :
			self.speed.setToolTip(self.tr._translate('Fast+'))
		elif i == 2 :
			self.speed.setToolTip(self.tr._translate('Fast'))
		elif i == 1 :
			self.speed.setToolTip(self.tr._translate('Normal'))
		else :
			self.speed.setToolTip(self.tr._translate('Slow'))

	def runBackUp(self):
		self.Parent.setTabsState(False)
		self.progress.show()
		self.runned = True
		mode = 0 if self.mode.currentIndex() else 1
		speed = SPEED[self.speed.currentIndex()]
		print 'BackUp running in %i mode and %i speed ...' % (mode, speed)
		self.t = QProcess()
		Data = QStringList()
		Data.append('/usr/share/thrifty/thrifty.py')
		opt = ''.join(('G:', str(USER_UID), '/', str(USER_GID), '::', str(speed)))
		Data.append(opt)
		self.t.finished.connect(self.showResult)
		if mode : self.t.start('python', Data)
		else : self.t.start('pkexec', Data)
		if self.t.waitForStarted() :
			self.runned = True
			#print self.t.state()
		else :
			self.showResult()

	def setState(self, state):
		self.mode.setEnabled(state)
		self.speed.setEnabled(state)
		self.editExcludes.setEnabled(state)
		self.start.setEnabled(state)
		self.descriptionTask.setEnabled(state)

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

	def editExcludesFile(self):
		self.Parent.setTabsState(False)
		mode = 0 if self.mode.currentIndex() else 1
		if mode :
			path_ = os.path.expanduser('~/.config/thrifty/thrifty.excludes')
		else :
			path_ = '/etc/thrifty.excludes'
		self.editor = Editor(path_, mode, self)
		self.editor.show()

	def enableEditorButton(self):
		self.Parent.setTabsState(True)
