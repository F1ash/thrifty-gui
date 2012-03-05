# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

SPEED = {
		'Slow'		: 2,
		'Normal'	: 1,
		'Fast'		: 0,
		'Fast+'		: 3
		}

class BackUp(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.Parent = parent

		self.layout = QGridLayout()

		self.buttonLayout = QVBoxLayout()
		self.mode = QComboBox()
		self.mode.setToolTip('Mode of task')
		self.mode.addItems(QStringList() << 'User' << 'Root')
		self.speed = QComboBox()
		self.speed.addItems(QStringList() << 'Slow' << 'Normal' << 'Fast' << 'Fast+')
		self.speed.setToolTip('Speed of task execution')
		self.editExcludes = QPushButton()
		self.editExcludes.setToolTip('Edit Excludes file for current regime')
		self.editExcludes.clicked.connect(self.editExcludesFile)
		self.start = QPushButton()
		self.start.clicked.connect(self.runBackUp)
		self.start.setToolTip('Start task')

		self.buttonLayout.addWidget(self.mode)
		self.buttonLayout.addWidget(self.speed)
		self.buttonLayout.addWidget(self.editExcludes)
		self.buttonLayout.addWidget(self.start)

		self.progress = QProgressBar()
		self.progress.setOrientation(Qt.Vertical)
		self.progress.hide()
		self.progress.setRange(0, 0)

		self.layout.addItem(self.buttonLayout, 0, 0)
		self.layout.addWidget(self.progress, 0, 1)

		self.setLayout(self.layout)

	def runBackUp(self):
		self.Parent.setTabsState(False)
		self.progress.show()
		mode = 0 if self.mode.currentIndex() else 1
		speed = SPEED[str(self.speed.currentText())]
		print 'BackUp running in %i mode and %i speed ...' % (mode, speed)
		''' запустить поток и по сигналу включить закладки '''
		QTimer.singleShot(5000, self.qwerty)

	def setState(self, state):
		self.mode.setEnabled(state)
		self.speed.setEnabled(state)
		self.editExcludes.setEnabled(state)
		self.start.setEnabled(state)

	def qwerty(self):
		self.Parent.setTabsState(True)
		self.progress.hide()

	def editExcludesFile(self): pass
