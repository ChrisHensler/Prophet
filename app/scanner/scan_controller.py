import uuid
import subprocess
import os
import nmap_parser
import nmap_xml_parser
import web_scanner
from app.util import fileutil

APP_ROOT = '.'

def Run(name, flags, ip_list):

	scan_guid = str(uuid.uuid1())
	
	print "Starting scan: " + scan_guid
	print "Scan Type: " + name

	cmd = "%s %s %s %s %s" % ('nmap', flags, ip_list, '-oA', fileutil.getTmpPath() + str(scan_guid))
	print 'running: ' + cmd

	subprocess.call(cmd.split(' '))

	ParseScan(scan_guid)


def RunAll(ip_list = '-iL ' + fileutil.getConfigPath() + 'ip_list'):
	print "SCANNING RANGE: " + ip_list

	#get scan profiles
	with open(fileutil.getConfigPath() + 'scan_profiles', 'r') as scan_file:
		for scan in scan_file:
			#confirm valid format and not a comment
			if(':' in scan and not scan.startswith('#')):
				#run scan
				profile = scan.rstrip('\n').split(':')
				Run(profile[0],profile[1],ip_list)

	web_scanner.ScanAll()

	
def ParseScan(scan):
	path = fileutil.getTmpPath() + scan + '.xml'
	if os.path.exists(path):
		nmap_xml_parser.parseXML(path)
	else:
		print 'Cannot parse scan: file does not exist'
