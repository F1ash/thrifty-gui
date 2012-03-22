# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from StatusBar import StatusBar
from Translator import Translator
from Functions import randomString, readFile, USER_UID, USER_GID
import os, os.path

class Editor(QMainWindow):
	def __init__(self, path = '', mode = 1, parent = None, task = None):
		QMainWindow.__init__(self, parent)
		self.tr = Translator('Thrifty')

		#self.resize(450, 350)
		self.setWindowTitle(self.tr._translate('Thrifty'))
		self.setWindowIcon(QIcon('/usr/share/thrifty/icons/sniper_soldier.png'))

		self.save_ = QAction(QIcon('/usr/share/thrifty/icons/save.png'), self.tr._translate('&Save'), self)
		self.save_.setShortcut('Ctrl+S')
		self.save_.setStatusTip(self.tr._translate('Save file'))
		self.connect(self.save_, SIGNAL('triggered()'), self._save)

		self.exit_ = QAction(QIcon('/usr/share/thrifty/icons/exit.png'), self.tr._translate('&Exit'), self)
		self.exit_.setShortcut('Ctrl+Q')
		self.exit_.setStatusTip(self.tr._translate('Exit application'))
		self.connect(self.exit_, SIGNAL('triggered()'), self._close)

		self.giveToYum = QAction(QIcon('/usr/share/thrifty/icons/exit.png'), self.tr._translate('to &Yum'), self)
		self.giveToYum.setShortcut('Ctrl+Y')
		self.giveToYum.setStatusTip(self.tr._translate('Give package list to Yum for reinstall'))
		self.connect(self.giveToYum, SIGNAL('triggered()'), self.runYum)
		self.giveToYum.setEnabled(False)

		menubar = self.menuBar()

		file_ = menubar.addMenu(self.tr._translate('&File'))
		file_.addAction(self.save_)
		file_.addAction(self.exit_)

		toYum = menubar.addMenu(self.tr._translate('&Action'))
		toYum.addAction(self.giveToYum)

		if task is not None :
			self.save_.setEnabled(False)
			if task : self.giveToYum.setEnabled(True)

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
				_s = [s_ + '\n' for s_ in l]
				_s.sort()
				s = ''.join(_s)
		#print [s, QString().fromUtf8(s)]
		self.editor.setPlainText(QString().fromUtf8(s))
		self.statusBar.showMessage('Edit : ' + self.path)

	def runYum(self):
		self.save_.setEnabled(False)
		self.exit_.setEnabled(False)
		self.giveToYum.setEnabled(False)
		packageList = self.editor.toPlainText()
		self.editor.clear()
		self.editor.setReadOnly(True)
		Data = QStringList()
		Data.append('yum')
		Data.append('-y')
		Data.append('reinstall')
		for item in packageList.split('\n') :
			if item != '' :
				#print [item]
				Data.append(item)
		## run yum in dispatched process
		self.y = QProcess()
		self.y.readyReadStandardOutput.connect(self.appendOutputString)
		self.y.readyReadStandardError.connect(self.appendErrorString)
		self.y.finished.connect(self.showResult)
		self.y.start('pkexec', Data)
		if self.y.waitForStarted() :
			#print self.y.state()
			self.statusBar.showMessage(self.tr._translate('Yum runned...'))
		else :
			self.showResult()

	def appendOutputString(self):
		output = self.y.readAllStandardOutput()
		self.editor.append(QString().fromUtf8(output))

	def appendErrorString(self):
		error = self.y.readAllStandardError()
		self.editor.append(QString().fromUtf8(error))

	def showResult(self):
		self.exit_.setEnabled(True)
		self.statusBar.showMessage(self.tr._translate('Ready to exit.'))

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
		self.statusBar.showMessage(self.tr._translate('Exit code: ') + str(self.s.exitCode()))

	def _close(self):
		self.Parent.enableEditorButton()
		self.close()

	def closeEvent(self, e):
		self.Parent.enableEditorButton()
		e.accept()
