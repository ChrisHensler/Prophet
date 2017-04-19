#!/usr/bin/env python

import app.scanner.scan_controller as scan_controller
from app.util import clean,info

sep = "-------------"

living = True
while living:
	cmd = raw_input().split(' ')
	first = cmd[0].lower()
	if len(first.strip()) > 0:
		print sep

		if(first == "scan"):
			scan_controller.RunAll()

		elif(first == "parse"):
			scan_controller.ParseScan(cmd.split(' ')[1])

		elif(first == "clean"):
			clean.clean()

		elif(first == "info"):
			host = None
			port = None

			if(len(cmd) > 1):
				host = cmd[1]
			if(len(cmd) > 2):
				port = cmd[2]

			print info.getInfoString(host,port)

		elif(first in ["exit","quit"]):
			living = False
			print "Goodbye"
		#must be last
		else:
			print("Valid commands are:")
			print("Scan: runs scan")
			print("Parse <scan id>: update reports based on the scan id")
			print("Info <host> <port>: show info on host and optionally port")
			print("Exit: End Program")

		print sep
		
