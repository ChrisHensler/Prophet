import uuid
import subprocess
import os
import nmap_parser

def scan():
	print "SCANNING SYSTEM INFO__________________ "
	scan_guid = uuid.uuid1()
	scan_results_file = '../tmp/'+str(scan_guid)
	scan_results_file2 = scan_results_file + '.OS'

	print "storing tmp files in: " + scan_results_file

	subprocess.call(['nmap', '-iL', nmap_parser.get_iplist_location(), '-A', '-oG', scan_results_file, '-oN', scan_results_file2] )

	nmap_parser.parseGrepable(scan_results_file)
	nmap_parser.parseOSScan(scan_results_file2)
