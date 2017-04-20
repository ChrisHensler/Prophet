import shutil
import os
import fileutil
import socket
import color
import re

DEBUG=False

HOST_INFO_STRING = """
{0}

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


def listHosts():
	path = fileutil.getPortPath(None, None)
	info = ""

	p = os.listdir(path)

	#sort ip addresses
	p = sorted(p,key=lambda item: socket.inet_aton(item))

	for filename in p:
		info += filename.split('/')[-1] + '\n'

	return color.white + info + color.neutral

def getInfoString(host, port=None):
	if host is None: return listHosts()
	detail_port = not port is None
	#display host details only if not infoing port or infoing everything
	detail_host = True
	if not port is None:
		detail_host = (port == 'all')
		
	info = getInfoObj(host, detail_port)

#	if(port is None):
#		scanstring = ""
#		for portObj in sorted(info["ports"], key=lambda x: int(x["name"].split(".")[1])):
#			scanstring += parsePortObj(portObj)
#		scanstring += color.magenta + "_"*40 + color.neutral + '\n'
#
#		#host level scripts
#		for script in info["scan_results"]:	
#				scanstring += getScanString(script["name"],script["text"])
#		host_header = color.white + '_'*15 + host + '_'*15 + color.neutral
#		infostring = HOST_INFO_STRING.format(host_header, scanstring, info["system_info"])
#
#	else:
#		infostring = ""
#		for portObj in info["ports"]:
#			if port in portObj["name"]:
#				infostring += parsePortObj(portObj)

	infostring = ""
	for portObj in sorted(info["ports"], key=lambda x: int(x["name"].split(".")[1])):
		#port filter
		if port is None or port == 'all' or port in portObj["name"]:	
			infostring += parsePortObj(portObj)

	infostring += color.magenta + "_"*40 + color.neutral + '\n'

	#host level scripts
	if detail_host:
		scanstring = "Host Scan:"
		for script in info["scan_results"]:
				scanstring += getScanString(script["name"],script["text"])
				host_header = color.white + '_'*15 + host + '_'*15 + color.neutral
				#reformat infostring to host template
				infostring = HOST_INFO_STRING.format(host_header, infostring, info["system_info"])
	return infostring


def parsePortObj(portObj):
	port_header = color.magenta + (portObj["name"].upper() + ("_" * 40))[:40] + "\n" + color.neutral
	if DEBUG: print str(portObj["service_info"])
	scanstring = port_header

	for key in portObj["service_info"]:
		scanstring += "{0}: {1}\n".format(key.replace('_',' '),portObj["service_info"][key])

	for script in portObj["scan_results"]:	
		scanstring += getScanString(script["name"],script["text"])

	return scanstring

def getScanString(name, text):
	#highlight vulns
	vuln_token='//<vuln_aveqvd>//'
	vuln_regex = re.compile('vulnerable', re.IGNORECASE)
	text = re.sub(vuln_regex,vuln_token, text)
	notvuln_regex = re.compile('not '+vuln_token, re.IGNORECASE)
	text = re.sub(notvuln_regex, color.string(color.yellow, 'NOT VULNERABLE'), text)
	text = re.sub(vuln_token, color.string(color.red, 'VULNERABLE'), text)

	#important things I want to know
	important_things = ['Script execution failed (use -d to debug)','Forbidden']
	for thing in important_things:
		text.replace(thing, color.string(color.orange, thing))


	return "\n{2}{0}{3}\n______________\n{1}\n_________\n".format(name,text, color.yellow, color.neutral)

