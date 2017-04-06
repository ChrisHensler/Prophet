import os
import re

def parseGrepable(scan_results_file):
	#parse nmap grepable output
	print "ANALYZING GREPABLE_______________"
	print scan_results_file
	print "_______________________"

	f = open(scan_results_file, 'r')
	for line in f:
		#register new host
		if('Up' in line): 
			host = '../out/' + line.split(' ')[1]
			if not os.path.exists(host):
				os.makedirs(host)
		#register ports			
		if('/open/' in line):
			print "PARSING: " + line
			host = '../out/' + line.split(' ')[1]
			print host
			if not os.path.exists(host):
				os.makedirs(host)

			#parse ports
			port_section = line[line.index("Ports: ") + 7:]
			for portstring in port_section.split(','):
				print "portline: " + portstring
				portinfo = portstring.split('/')
				if(portinfo[1] == "open"):					
					portpath = host + "/" + portinfo[2].strip() + "-" + portinfo[0].strip()
					if(len(portinfo) > 3):
						portpath = portpath + "-" + portinfo[4].strip()

					print "resolved: " + portpath

					if not os.path.exists(portpath):
						os.makedirs(portpath)

	f.close()
	compileDependants()

def parseOSScan(scan_results_file):
	print "ANALYZING OS SCAN_______________"
	print scan_results_file
	print "_______________________"

	#context variables
	host = ""
	record=True
	scan_results = ""

	with open(scan_results_file, 'r') as f:
		for line in f:
			possible_host = parseHost(line)
			if len(possible_host) > 0 and possible_host != host:
				#write old file
				if(host != ""):
					print "Writing host"
					sysdir = "../out/"+host+"/system_info/"
					if not os.path.exists(sysdir):
						os.makedirs(sysdir)
					with open(sysdir + "os_scan.results.txt", 'w') as hostfile:
						hostfile.write(scan_results)
			
				#set new host
				host = possible_host
				scan_results = ""
				print "Found host: " + host

			if record:
				scan_results = scan_results + line + "\n" 

	compileDependants()


def isIp(s):
	match = getIp(s)
	if match and s!="":
		return len(match) == len(s)
	return False	

def getIp(s):
	m=re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}\b",s)
	if m:
		return m.group()

def parseHost(line):
	ip =""
	if "Nmap scan report" in line:
		ip = getIp(line)
	return ip

def parseAll():
	for item in os.listdir("../tmp"):
		if item.endswith(".OS"):
			parseOSScan("../tmp/" +item)
		else:
			parseGrepable("../tmp/" +item)
				

def compileDependants():
	iplist_loc = get_iplist_location()
	print "COMPILING " + iplist_loc

	ip_list_content = ""
	for item in os.listdir("../out"): 
		if isIp(item): #only IP addresses expected
			ip_list_content = ip_list_content + item + "\n"
		else:
			print "FOUND ATTEMPTED NON-IP IN ip_list"
		
	ip_list_content = ip_list_content
	with open(iplist_loc,"w") as f:
		f.truncate()
		f.write(ip_list_content)

def get_iplist_location():
	return "../out/ip_list"

