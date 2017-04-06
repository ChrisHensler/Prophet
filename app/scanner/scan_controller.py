import uuid
import subprocess
import os
import nmap_parser


APP_ROOT = '.'


def Run(name, flags, ip_list):
	print "Starting scan: " + name

	scan_guid = uuid.uuid1()
	scan_results_file = APP_ROOT + '/tmp/'+str(scan_guid)
	print "storing tmp files in: " + scan_results_file
	
	cmd = "%s %s %s %s %s" % ('nmap', flags, ip_list, '-oA', scan_results_file)
	print 'running: ' + cmd

	#with open(os.devnull, "w") as output:
	subprocess.call(cmd.split(' '))

	nmap_parser.parseGrepable(scan_results_file + '.gnmap')

def RunAll(ip_list = '-iL ' + APP_ROOT + '/etc/ip_list'):
	print "scanning range" + ip_list

	#get scan profiles
	with open(APP_ROOT + '/etc/scan_profiles', 'r') as scan_file:
		for scan in scan_file:
			#confirm valid format and not a comment
			if(':' in scan and not scan.startswith('#')):
				#run scan
				profile = scan.rstrip('\n').split(':')
				Run(profile[0],profile[1],ip_list)
	
