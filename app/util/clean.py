import shutil
import os
import fileutil

def clean():
	cleanOut()

	outdir=fileutil.getTmpPath()
	cleanTmp()

	cleanFile("hydra.restore")


	print "WE ARE NOW CLEAN!"

def cleanTmp():
	cleanDir(fileutil.getTmpPath())

def cleanOut():
	cleanDir(fileutil.getOutPath())

def cleanDir(outdir):
	if os.path.exists(outdir):
		shutil.rmtree(outdir)
	os.makedirs(outdir)

def cleanFile(path_from_root):
	path=os.path.join(fileutil.getRootPath(), path_from_root)
	if os.path.exists(path):
		os.remove(path)
