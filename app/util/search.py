from app.util import info, color
import docopt

DEBUG=False

#todo: add OS search
def search(ports=None, os=None):
	hoststring = ""
	for host in info.getHosts():
		host_info = info.getInfoObj(host, detailed=True)
		h = parseHostString(host_info, ports, os)
		if h: hoststring += h + '\n\n'
	return hoststring

def checkFilter(filterString, value):
	if(filterString is None): return False
	filterArr=filterString.split(',')

	if DEBUG: print "checking filter: " + str(filterArr) + " on " + str(value)

	return value in filterArr;

def parseHostString(hostObj, filter_ports, filter_os):
	infostring = ""
	host = hostObj["name"]

	port_filter_passed = filter_ports is None
	os_filter_passed = filter_os is None

	for portObj in sorted(hostObj["ports"], key=lambda x: int(x["name"].split(".")[1])):
		p = parsePortObj(portObj, filter_ports)
		if p:
			port_filter_passed = True
			infostring += p

	infostring += info.port_color + "_"*40 + color.neutral + '\n'

	#host level scripts
	host_header = info.host_color + '_'*15 + host + '_'*15 + color.neutral

	scanstring=""
	if not (filter_os is None or hostObj["system_info"] is None) and filter_os in hostObj["system_info"].lower():
		os_filter_passed = True
		scanstring += hostObj["system_info"]

	#reformat infostring to host template
	infostring = info.HOST_INFO_STRING.format(host_header, infostring, scanstring)

	if port_filter_passed and os_filter_passed:
		return infostring
	else:
		return ""
	

def parsePortObj(portObj, filter_ports):
	#port filter
	if not checkFilter(filter_ports, portObj["name"].split('.')[1]):
		return ""

	port_header = info.port_color + (portObj["name"].upper() + ("_" * 40))[:40] + "\n" + color.neutral
	scanstring = port_header

	for key in portObj["service_info"]:
		scanstring += "{0}: {1}\n".format(key.replace('_',' '),portObj["service_info"][key])

	return scanstring


