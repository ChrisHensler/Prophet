import discovery
import clean
import sysscan
import sys
import nmap_parser

if("-p" in sys.argv): #parse only(used mainly for dev)
	nmap_parser.parseAll()
else:

	if(not "-nC" in sys.argv):
		#prep environment
		clean.clean()

	if(not "-nD" in sys.argv):
		#discover hosts
		discovery.discover()

	if(not "-nS" in sys.argv):
		#get system info for discovered machines
		sysscan.scan()


