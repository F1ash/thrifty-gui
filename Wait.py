# -*- coding: utf-8 -*-

from PyQt4.QtCore import QThread
from signal import SIGTERM
from time import sleep
import os

def pid_exists(pid, sig):
	try:
		os.kill(pid, sig)
		return True
	except OSError, err:
		return False

class Wait(QThread):
	def __init__(self, pid = 0, parent = None):
		QThread.__init__(self, parent)

		self.Parent = parent
		self.pid = pid
		self.stop = False

	def run(self):
		while True :
			if pid_exists(self.pid, 0) :
				if self.stop :
					pid_exists(self.pid, SIGTERM)
					break
				else : sleep(1)
			else : break
		if self.Parent is not None : self.Parent.stop.emit()

	def __del__(self):
		self.stop = True
