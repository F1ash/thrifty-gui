# -*- coding: utf-8 -*-

import os, sys, os.path
from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, S_IWOTH

def setFileState(name_):
	os.chmod(name_, S_IROTH | S_IWUSR |  S_IRGRP | S_IWGRP | S_IRUSR | S_IWOTH)


if __name__ == '__main__':
	parameters = sys.argv
	if len(parameters) > 2 :
		print parameters[1], len(parameters)
		try :
			fileName = parameters[2]
			with open(parameters[1], 'wb') as f :
				with open(fileName, 'rb') as g :
					f.write(g.read())
			if os.path.isfile(parameters[1]) :
				setFileState(parameters[1])
			if os.path.isfile(fileName) :
				os.remove(fileName)
		except Exception, err :
			print err
		finally : pass
