import uuid
import subprocess
import os
import nmap_parser
import generic_scanner
from app.util import fileutil, color
from app.cracker import crack_controller

APP_ROOT = '.'

#run nmap scan. nmap scans are the backbone of the program and must be run in sequence
def Run(name, flags, ip_list):

	scan_guid = str(uuid.uuid1())
	
	print "Starting scan: " + scan_guid
	print "Scan Type: " + name

	cmd = "%s %s %s %s %s" % ('nmap', flags, ip_list, '-oA', fileutil.getTmpPath() + str(scan_guid))
	print 'running: ' + color.string(color.interesting_color, cmd)

	#whitespace strip
	c = []
	for i in cmd.split(' '):
		if not i.strip()=='':
			c.append(i)
	subprocess.call(c)

	ParseScan(scan_guid)


def RunAll(ip_list = '-iL ' + fileutil.getConfigPath() + 'ip_list'):
	print "SCANNING RANGE: " + ip_list

	#get scan profiles
	with open(fileutil.getConfigPath() + 'scan_profiles', 'r') as scan_file:
		for scan in scan_file:
			if scan.startswith("~web"):
				generic_scanner.ScanAll(name="nikto", action="nikto -host {host} -port {port}", valid_services=['http'])
				
				wordlist = fileutil.getConfigPath() + 'web_discovery_wordlist.txt'
				wfuzz = "wfuzz -c -z file," + wordlist + " --hc 404 {host}:{port}/FUZZ"
				generic_scanner.ScanAll(name="wfuzz", action=wfuzz, valid_services=['http'])

			elif scan.startswith("~snmp"):
				generic_scanner.ScanAll(name="snmp_check", action="snmp-check -t {host} -c public", valid_ports=['161'])

			elif scan.startswith("~smb"):
				generic_scanner.ScanAll(name="smb_enum", action="enum4linux -a -R 500-550,1000-1050,3000-3050 {host}", valid_ports = ['139','445'], run_once=True)
				
			elif scan.startswith("~defaults"):
				for host in fileutil.getSubDirs(fileutil.getPortPath(None,None)):
					crack_controller.crackDefaults(host)

			#confirm valid format and not a comment
			elif(':' in scan and not scan.startswith('#')):
				#run scan
				profile = scan.rstrip('\n').split(':')
				Run(profile[0],profile[1],ip_list)

def ParseScan(scan):
	path = fileutil.getTmpPath() + scan + '.xml'
	if os.path.exists(path):
		nmap_parser.parseXML(path)
	else:
		print 'Cannot parse scan: file does not exist'
