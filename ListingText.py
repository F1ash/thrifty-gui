# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ListingText(QDialog):
	def __init__(self, text = '', parent = None):
		QDialog.__init__(self, parent)

		browseText = QTextEdit()
		browseText.setReadOnly(True)
		browseText.setMinimumWidth(750)

		browseText.setText(text)

		form = QGridLayout()
		form.addWidget(browseText,0,0)
		self.setLayout(form)

	def closeEvent(self, event):
		event.ignore()
		self.done(0)

