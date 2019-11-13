import shutil
import os
import app.util.fileutil

def progress():
	for f in os.listdir(fileutil.getTmpPath()):
		if f.startswith('__'):
			v = f.split('__')
			if len(v) > 3:
				print("{0}:\t{1}:{2}".format(v[1],v[2], v[3]))
