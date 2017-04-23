import zipfile
import fileutil
import os
import clean

DEBUG=False


def getSaveFileName(name):
	return fileutil.getSavePath() + name + '.zip'

def save(name, overwrite = False):
	zpath = getSaveFileName(name)
	opath = fileutil.getOutPath()

	#check existence of file and confirm overwrite
	if os.path.exists(zpath) and not overwrite:
		print name + " exists. Are you sure you want to overwrite? (Y/n)"
		resp = raw_input()
		#starts with y or is whitespace
		if not (resp.lower().startswith('y') or len(resp.strip())==0):
			print 'cancelling save'
			return
	print 'saving workspace: ' + name
	print opath
	with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
		for root, dirs, files in os.walk(opath):
			for f in files:
				z.write(os.path.relpath(os.path.join(root,f)))

def load(name):	
	#backup current
	save('__last__', overwrite = True)

	zpath = getSaveFileName(name)
	opath = fileutil.getRootPath()	#needs to be root because the out dir exists in the zip
	
	#clear out
	clean.cleanOut()

	print "loading..."
	with zipfile.ZipFile(zpath) as z:
		z.extractall(path=opath)
	print "load successful!"
