# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from StatusBar import StatusBar
from Functions import randomString, readFile, USER_UID, USER_GID
import os, os.path

class Editor(QMainWindow):
	def __init__(self, path = '', mode = 1, parent = None, task = None):
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

		self.giveToPk = QAction(QIcon('/usr/share/thrifty/icons/exit.png'), '&to PKit', self)
		self.giveToPk.setShortcut('Ctrl+P')
		self.giveToPk.setStatusTip('Give package list to PackageKit for reinstall')
		self.connect(self.giveToPk, SIGNAL('triggered()'), self.runPKit)
		self.giveToPk.setEnabled(False)

		menubar = self.menuBar()

		file_ = menubar.addMenu('&File')
		file_.addAction(self.save_)
		file_.addAction(self.exit_)

		toPK_ = menubar.addMenu('&Action')
		toPK_.addAction(self.giveToPk)

		if task is not None :
			self.save_.setEnabled(False)
			if task : self.giveToPk.setEnabled(True)

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
		if task is None :
			s = readFile(self.path)
		else : 
			s_ = readFile(self.path)
			if self.path == '' :
				s = s_
			else :
				l = []
				for item in s_.split('\n') :
					chunks = item.split(' ')
					if len(chunks) >= task + 1 :
						if chunks[task] != '' and chunks[task] not in l:
							l.append(chunks[task])
				s = ''.join([s_ + '\n' for s_ in l])
		#print [s, QString().fromUtf8(s)]
		self.editor.setPlainText(QString().fromUtf8(s))
		self.statusBar.showMessage('Edit : ' + self.path)

	def runPKit(self):
		packageList = self.editor.toPlainText()
		for item in packageList.split('\n') :
			if item != '' : print [item]

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
