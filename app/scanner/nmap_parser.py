#!/usr/bin/env python

import subprocess
import xml.etree.ElementTree as ET
import json
import app.util.fileutil as fileutil
import app.util.color as color

VERBOSE = False
DEBUG = False


def parseIpRange(ip_range):
	toReturn = []
	p = subprocess.check_output(['nmap','-sL','-n',ip_range])
	for line in p.split(b'\n'):
		if b'scan report' in line:
			toReturn.append(line.split(b' ')[4])
	return toReturn

def parseXML(scan_results_file):
	#parse nmap grepable output
	print("ANALYZING XML_______________")
	print(scan_results_file)
	try:
		parsed = ET.parse(scan_results_file)

		root = parsed.getroot()
	except:
		color.c_print(color.bad_color, "Error parsing XML!")
		return

	
	for host in root.findall('host'):
		#create file, if not exists
		hostpath = fileutil.getRemoteOutPath() + str(host.find('address').get('addr'))
		fileutil.mkdir(hostpath)

		#port services
		makePortDirs(host, hostpath)

		for hostscript in host.iter('hostscript'):
			storeScriptResults(hostscript, hostpath)

	print("Done!")

def makePortDirs(host, hostpath):
	if DEBUG: print("MAKING PORT DIRECTORIES")
	if(not hostpath.endswith('/')):
		hostpath = hostpath + '/'

	for port in host.iter('port'):
			state = port.find('state').get('state')
			if (state == 'open'):
				service = port.find('service')
				portpath = hostpath + str(port.get('protocol')) + '.' + str(port.get('portid')) + '.' + str(service.get('name'))
				if DEBUG: print("ADDING " + portpath)

				#create file, if not exists
				fileutil.mkdir(portpath)

				#store service info
				aggServiceInfo(portpath, service)

				storeScriptResults(port, portpath)
	#parse host level things
	has_os_guess = False
	guess_string = "OS Guesses:\n"
	for osmatch in host.iter('osmatch'):
		has_os_guess = True
		guess_string += osmatch.get("accuracy") + "%: " + osmatch.get("name") + "\n"

	uptime = host.find("uptime")
	uptime_string = ""
	if not uptime is None:
		uptime_string = "\n\nUptime: " + uptime.get("seconds") + "s Last boot: " + uptime.get("lastboot") + "\n"

	#write system_info file if we actually have information
	#todo: implement some kind of merge system
	if has_os_guess:
		host_info_string = guess_string + uptime_string
		fileutil.writeTo(hostpath + 'system_info.txt', host_info_string)

def aggServiceInfo(servicepath, serviceNode):
	if(not servicepath.endswith('/')):
		servicepath = servicepath + '/'

	filepath = servicepath + 'service_info.json'

	#if exists, get old info
	info = fileutil.readAsJSON(filepath)
	
	#load new info
	for attr in ["name","product","version","ostype"]:
		attrValue = str(serviceNode.get(attr))
		if not attrValue.lower() in ["","none"]:
			info[attr] = attrValue
	#save
	fileutil.writeJSONTo(filepath, info)

def storeScriptResults(xmlContext, path):
	if(not path.endswith('/')):
		path = path + '/'

	for script in xmlContext.findall('script'):
		#fileutil.writeXMLTo(path + script.get('id') + '.scan.xml',script)
		fileutil.writeTo(path + script.get('id') + '.nse.scan.txt',str(script.get('output')))
