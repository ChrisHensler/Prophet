#!/usr/bin/env python

import app.scanner.scan_controller as scan_controller
from app.util import clean,info, workspaces, update

sep = "-------------"

living = True
while living:
	cmd = raw_input().split(' ')
	first = cmd[0].lower()
	if len(first.strip()) > 0:
		print sep

		if(first == "scan"):
			if(len(cmd) > 1):
				scan_controller.RunAll(cmd[1])
			else:
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
		elif(first == "update"):
			update.update()
		elif(first == "save" and len(cmd) > 1):
			name = cmd[1]
			workspaces.save(name)

		elif(first == "load"  and len(cmd) > 1):
			name = cmd[1]
			workspaces.load(name)

		elif(first in ["exit","quit"]):
			living = False
			print "Goodbye"
		#must be last
		else:
			print("Valid commands are:")
			print("Scan <ip range>: runs scan")
			print("Parse <scan id>: update reports based on the scan id")
			print("Info <host> <port>: show info on host and optionally port")
			print("Info <host> all: show info on host and all ports")
			print("Save <name>: saves a scan with the given name")
			print("Load <name>: loads a saved scan")
			print("update: updates dependants, such at NSE scripts")
			print("Exit: End Program")

		print sep
		
