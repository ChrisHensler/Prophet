import shutil
import os
import fileutil

def clean():
	print "CLEANING OUTPUT DIRECTORY..."
	cleanOut()

	outdir=fileutil.getTmpPath()
	print "CLEANING TMP DIRECTORY..."
	cleanTmp()

	print "Done!"

def cleanTmp():
	cleanDir(fileutil.getTmpPath())

def cleanOut():
	cleanDir(fileutil.getOutPath())

def cleanDir(outdir):
	if os.path.exists(outdir):
		shutil.rmtree(outdir)
	os.makedirs(outdir)
