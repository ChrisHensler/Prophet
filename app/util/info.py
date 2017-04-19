import shutil
import os
import fileutil

DEBUG=False

HOST_INFO_STRING = """
INFO ON HOST: {0}

{1}
{2}
"""

def getInfoObj(host, detailed = True):
	info = {}
	path = fileutil.getPortPath(host, None)

	#get sysinfo
	info["system_info"] = fileutil.read(os.path.join(path,'system_info.txt'))
	info["ports"] = []
	info["scan_results"] = getScanResults(path)
	#get ports(if host), recurse if requested
	for filename in os.listdir(path):
		filepath = os.path.join(path, filename)
		if os.path.isdir(filepath):
			info["ports"].append(getPortInfoObj(filepath, detailed))

	return info

def getPortInfoObj(portpath, detailed = True):
	portObj = {}
	portObj["name"] = portpath.split('/')[-1]
	portObj["service_info"] = fileutil.readAsJSON(os.path.join(portpath,'service_info.json'))
	if detailed:
		portObj["scan_results"] = getScanResults(portpath)
	else:
		portObj["scan_results"] = {}

	return portObj

def getScanResults(path):
	scan_results = []

	for scanFileName in os.listdir(path):
		scanFilePath = os.path.join(path, scanFileName)
		if os.path.isfile(scanFilePath) and scanFilePath.endswith(".scan.txt"):
			scanObj = {}
			scanObj["name"] = scanFilePath.split('/')[-1][:-9]
			scanObj["text"] = fileutil.read(scanFilePath)

			scan_results.append(scanObj)
	return scan_results

def getInfoString(host, port=None):
	info = getInfoObj(host, port!=None)

	if(port == None):
		scanstring = ""
		for portObj in sorted(info["ports"], key=lambda x: int(x["name"].split(".")[1])):
			scanstring += parsePortObj(portObj)

		#host level scripts
		for script in info["scan_results"]:	
				scanstring += "\n{0}\n______________\n{1}\n_________\n".format(script["name"],script["text"])

		infostring = HOST_INFO_STRING.format(host, scanstring, info["system_info"])

	else:
		infostring = ""
		for portObj in info["ports"]:
			if port in portObj["name"]:
				infostring += parsePortObj(portObj)
	
	return infostring



def parsePortObj(portObj):
	port_header = (portObj["name"].upper() + ("_" * 40))[:40] + "\n"
	if DEBUG: print str(portObj["service_info"])
	scanstring = port_header

	for key in portObj["service_info"]:
		scanstring += "{0}: {1}\n".format(key.replace('_',' '),portObj["service_info"][key])

	for script in portObj["scan_results"]:	
		scanstring += "\n{0}\n______________\n{1}\n_________\n".format(script["name"],script["text"])

	return scanstring

