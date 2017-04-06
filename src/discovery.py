import uuid
import subprocess
import os
import nmap_parser

def discover():
	print "DISCOVERY SCANS__________________ "
	scan_guid = uuid.uuid1()
	scan_results_file = '../tmp/'+str(scan_guid)
	print "storing tmp files in: " + scan_results_file

	subprocess.call(['nmap', '-sTU','--top-ports=100', '-iL', '../etc/ip_list',  '-oG', scan_results_file])
	nmap_parser.parseGrepable(scan_results_file)

	#scan a few top ports to catch any that prevent ping
	subprocess.call(['nmap', '-Pn', '--top-ports','10', '-iL', '../etc/ip_list', '--excludefile', nmap_parser.get_iplist_location(),  '-oG', scan_results_file])

	nmap_parser.parseGrepable(scan_results_file)
