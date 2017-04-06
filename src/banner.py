

def grab():
	print "DISCOVERY SCANS__________________ "
	scan_guid = uuid.uuid1()
	scan_results_file = '../tmp/'+str(scan_guid)
	print "storing tmp files in: " + scan_results_file

	subprocess.call(['nmap', '--script=banner-plus.nse','-iL', '../out/ip_list','-oX', scan_results_file])



