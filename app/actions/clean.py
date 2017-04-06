import shutil
import os

def clean():
	outdir="../out"
	print "CLEANING OUTPUT DIRECTORY__________"
	if os.path.exists(outdir):
		shutil.rmtree(outdir)
		os.makedirs(outdir)
	outdir="../tmp"
	print "CLEANING TMP DIRECTORY__________"
	if os.path.exists(outdir):
		shutil.rmtree(outdir)
		os.makedirs(outdir)
