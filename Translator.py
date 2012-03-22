# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
import locale, os.path

class Translator(QTranslator):
	def __init__(self, context = '', parent=None):
		QTranslator.__init__(self, parent)

		lang = locale.getdefaultlocale()[0][:2]
		self.load(QString(lang), QString('/usr/share/thrifty'), QString('qm'))
		self.context = context

	def _translate(self, sourceText):
		res = self.translate(self.context, sourceText)
		if len(res) == 0:
			res = QString(sourceText)
		return res
