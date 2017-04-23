import info

DEBUG=False


#todo: add OS search
def search(keywords=[], ports=[],scriptname=[]):
	relevant_hosts = []
	for host in info.getHosts():
		host_info = info.getInfoObj(host, detailed=True)
		if containsPort(host_info, ports) and containsKeyword(host_info, keywords):
			relevant_hosts.append(host_info)
		

def containsPort(host_info, ports):
	for port in host_info["ports"]:
		for desired_port in ports:
			if desired_port in port["name"]:
				return True
	return False

#note: multiword strings are accepted
def containsKeyword(host_info, keywords):
	infostring = getInfoString(host_info["name"])
	for word in keywords:
		if word in infostring:
			return True
	return False

def containsScriptnames(host_info, script_names):
	for script in host_info["scan_results"]:
		for name in script_names:
			if(name in script["name"]):
				return True

	for port in host_info["ports"]:
		for script in port["scan_results"]:
			for name in script_names:
				if(name in script["name"]):
					return True
	return False
