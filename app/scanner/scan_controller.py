import uuid
import subprocess
import os
import app.scanner.generic_scanner as generic_scanner
import app.scanner.nmap_parser as nmap_parser
import app.util.fileutil as fileutil
import app.util.color as color
import app.cracker.crack_controller as crack_controller

APP_ROOT = '.'

def checkHookScan(row, startsWith, valid_scans=None):
	return row.startswith("~web") and not valid_scans

def ParseScan(scan):
	path = fileutil.getTmpPath() + scan + '.xml'
	if os.path.exists(path):
		nmap_parser.parseXML(path)
	else:
		print('Cannot parse scan: file does not exist')

#run nmap scan. nmap scans are the backbone of the program and must be run in sequence
def Run(name, flags, ip_list):

	scan_guid = str(uuid.uuid1())

	print("Starting scan: " + scan_guid)
	print("Scan Type: " + name)

	cmd = "%s %s %s %s %s" % ('nmap', flags, ip_list, '-oA', fileutil.getTmpPath() + str(scan_guid))
	print('running: ' + color.string(color.interesting_color, cmd))

	#todo: do in non-shell way
	subprocess.call(cmd, shell=True)

	ParseScan(scan_guid)

class ScanController:
	def __init__(self):
		self.scanner = generic_scanner.GenericScanner()
	def __del__(self):
		del self.scanner

	def Run(self, name, flags, ip_list):
		Run(name, flags, ip_list)

	def RunAll(self, ip_range, valid_scans=None):
		print("SCANNING RANGE: " + ip_range)

		#get scan profiles
		with open(fileutil.getConfigPath() + 'scan_profiles', 'r') as scan_file:
			for scan in scan_file:
				if scan.startswith('#'):
					continue
				elif checkHookScan(scan, "~web", valid_scans):
					self.scanner.ScanAll(name="nikto", action="nikto -host {host} -port {port} -T x46 -timeout 5 -maxtime 1h", valid_services=['http'], ip_range=ip_range)
				
					wordlist = os.path.join(fileutil.getConfigPath(),'wordlists', 'web_discovery_wordlist.txt')
					wfuzz = "wfuzz -c -w " + wordlist + " --hc 404,000 {host}:{port}/FUZZ"
					self.scanner.ScanAll(name="wfuzz", action=wfuzz, valid_services=['http'], ip_range=ip_range)

				elif checkHookScan(scan, "~snmp", valid_scans):
					self.scanner.ScanAll(name="snmp_check", action="snmp-check -t {host} -c public", valid_ports=['161'], ip_range=ip_range)

				elif checkHookScan(scan, "~smb", valid_scans):
					self.scanner.ScanAll(name="smb_enum", action="enum4linux -a -R 500-550,1000-1050,3000-3050 {host}", valid_ports = ['139','445'], run_once=True, ip_range=ip_range)
				
				elif checkHookScan(scan, "~defaults", valid_scans):
					ips = nmap_parser.parseIpRange(ip_range)
					for host in fileutil.getSubDirs(fileutil.getPortPath(None,None)):
						if host in ips:
							crack_controller.crackDefaults(host)
				elif checkHookScan(scan, "~simple_crack", valid_scans):
					ips = nmap_parser.parseIpRange(ip_range)
					for host in fileutil.getSubDirs(fileutil.getPortPath(None,None)):
						if host in ips:
							crack_controller.crackSimpleNames(host)
				#confirm valid format and not a comment
				elif(':' in scan):
					#run scan
					profile = scan.rstrip('\n').split(':')
					s_name = profile[0]
					s_cmd = ":".join(profile[1:])
					if((not valid_scans) or s_name in valid_scans):
						self.Run(s_name, s_cmd, ip_range)
