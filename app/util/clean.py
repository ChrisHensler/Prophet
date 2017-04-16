import shutil
import os
import fileutil

def clean():
	outdir=fileutil.getOutPath()
	print "CLEANING OUTPUT DIRECTORY__________"
	if os.path.exists(outdir):
		shutil.rmtree(outdir)
	os.makedirs(outdir)

	outdir=fileutil.getTmpPath()
	print "CLEANING TMP DIRECTORY__________"
	if os.path.exists(outdir):
		shutil.rmtree(outdir)
	os.makedirs(outdir)
	print "Done!"
