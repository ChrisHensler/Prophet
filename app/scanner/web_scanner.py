import os
from app.util import fileutil

def ScanAll():
	for host in fileutil.getSubDirs(fileutil.getPortPath(None,None)):
		ScanHost(host)

def ScanHost(host):
	print "Starting nikto scan on " + host

	hpath = fileutil.getPortPath(host,None)
	for portdir in fileutil.getSubDirs(hpath):
		portinfo = portdir[0].split('-')
		
		port = portinfo[0].strip('-')
		proto = portinfo[-1].strip('-')
		if(proto == 'http'):
			filepath = getPath(host,port) + 'nikto.scan.txt'
			if(os.path.exists(filepath)):
				print "Nikto has already run for " +host + ":" + port
			else:
				os.subprocess.call("nikto -host " + host + "-port " + port + " > " + filepath + " 2>&1 &", shell=True)


