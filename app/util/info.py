import shutil
import os
import fileutil

def getInfo(host, port=None, recursive = false):
	info = {}

	#get sysinfo
	info["service info"] = getServiceInfo(host, port)

	#get ports(if host), recurse if requested
	if(port==None):
		[f for f in listdir(path) if isdir()]
	#get script info

def getServiceInfo(host, port):
	path = getPortPath(host,port)
	serviceinfo = fileutil.readAsJSON(os.path.join(path,'service_info.json'))
	return serviceinfo
