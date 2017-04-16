#!/usr/bin/env python

import xml.etree.ElementTree as ET
import json
from app.util import fileutil

VERBOSE = False

def parseXML(scan_results_file):
	#parse nmap grepable output
	print "ANALYZING XML_______________"
	print scan_results_file
	print "_______________________"

	root = ET.parse(scan_results_file).getroot()

	
	for host in root.findall('host'):
		#create file, if not exists
		hostpath = fileutil.getOutPath() + str(host.find('address').get('addr'))
		fileutil.mkdir(hostpath)

		#port services
		makePortDirs(host, hostpath)

		for hostscript in host.iter('hostscript'):
			storeScriptResults(hostscript, hostpath)


def makePortDirs(host, hostpath):
	if(not hostpath.endswith('/')):
		hostpath = hostpath + '/'

	for port in host.iter('port'):
			state = port.find('state').get('state');
			if (state == 'open'):
				service = port.find('service');
				portpath = hostpath + str(port.get('protocol')) + '-' + str(port.get('portid')) + '-' + str(service.get('name'))

				#create file, if not exists
				fileutil.mkdir(portpath);

				#store service info
				aggServiceInfo(portpath, service)

				storeScriptResults(port, portpath);
	#parse host level things
	host_info_string = "OS Guesses:\n"
	for osmatch in host.iter('osmatch'):
		host_info_string = host_info_string + osmatch.get("accuracy") + "%: " + osmatch.get("name") + "\n"

	uptime = host.find("uptime")
	host_info_string = host_info_string + "\n\nUptime: " + uptime.get("seconds") + "s Last boot: " + uptime.get("lastboot") + "\n"


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
		if(attrValue != ""):
			info[attr] = attrValue
	#save
	fileutil.writeJSONTo(filepath, info)

def storeScriptResults(xmlContext, path):
	if(not path.endswith('/')):
		path = path + '/'

	for script in xmlContext.findall('script'):
		#fileutil.writeXMLTo(path + script.get('id') + '.scan.xml',script)
		fileutil.writeTo(path + script.get('id') + '.scan.txt',str(script.get('output')))
