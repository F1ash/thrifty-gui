# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from StatusBar import StatusBar
from Functions import randomString, readFile, USER_UID, USER_GID
import os, os.path

class Editor(QMainWindow):
	def __init__(self, path = '', mode = 1, parent = None):
		QMainWindow.__init__(self, parent)

		#self.resize(450, 350)
		self.setWindowTitle('ThriftyEditor')
		self.setWindowIcon(QIcon('/usr/share/thrifty/icons/sniper_soldier.png'))

		self.save_ = QAction(QIcon('/usr/share/thrifty/icons/save.png'), '&Save', self)
		self.save_.setShortcut('Ctrl+S')
		self.save_.setStatusTip('Save file')
		self.connect(self.save_, SIGNAL('triggered()'), self._save)

		self.exit_ = QAction(QIcon('/usr/share/thrifty/icons/exit.png'), '&Exit', self)
		self.exit_.setShortcut('Ctrl+Q')
		self.exit_.setStatusTip('Exit application')
		self.connect(self.exit_, SIGNAL('triggered()'), self._close)

		menubar = self.menuBar()

		file_ = menubar.addMenu('&File')
		file_.addAction(self.save_)
		file_.addAction(self.exit_)

		self.editor = QTextEdit(parent = self)
		self.setCentralWidget(self.editor)

		self.statusBar = StatusBar(self)
		self.setStatusBar(self.statusBar)

		self.Parent = parent
		self.mode = mode
		self.path = path
		self.editor.setUndoRedoEnabled(True)
		self.editor.setOverwriteMode(True)
		self.editor.createStandardContextMenu()
		s = readFile(self.path)
		#print [s, QString().fromUtf8(s)]
		self.editor.setPlainText(QString().fromUtf8(s))
		self.statusBar.showMessage('Edit : ' + self.path)

	def _save(self):
		text = self.editor.toPlainText()
		if self.mode :
			with open(self.path, 'wb') as f :
				f.write(text.toUtf8().data())
		else :
			fileName = os.path.join('/tmp', randomString(12))
			with open(fileName, 'wb') as f :
				f.write(text.toUtf8().data())
			self.s = QProcess()
			Data = QStringList()
			Data.append('/usr/bin/python')
			Data.append('/usr/share/thrifty/saveHelper.py')
			Data.append(self.path)
			Data.append(fileName)
			self.s.finished.connect(self.showExitCode)
			#for i in xrange(Data.count()) :
			#	print Data[i],
			#print
			self.s.start('pkexec', Data)
			if self.s.waitForStarted() :
				print 'status %s' % self.s.state()
			else :
				print '%s not saved' % self.path
				self.showExitCode()

	def showExitCode(self):
		self.statusBar.showMessage('Exit code: ' + str(self.s.exitCode()))

	def _close(self):
		self.Parent.enableEditorButton()
		self.close()

	def closeEvent(self, e):
		self.Parent.enableEditorButton()
		e.accept()
