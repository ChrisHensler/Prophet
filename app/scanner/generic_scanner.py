import os
import subprocess
import app.util.fileutil
import app.util.color
import app.scanner.nmap_parser
import datetime
from threading import Lock
from multiprocessing import Pool

debug = False

def parseCommand(cmd="", scan_name='Unknown', host='Unknown', port=None, outfile="/dev/null"):
			print("RUNNING {0} SCAN ON {1}:{2}".format(scan_name, host, str(port)))
			if debug: " to " + outfile
			print("scan will run in the background")

			#procfile should exist while the process is running so we can track the process
			procfile = "{4}__{0}__{1}__{2}__{3}__.proc".format(scan_name.replace(' ', '_'),host,port,str(datetime.datetime.now()).replace(' ','_'), fileutil.getTmpPath())

			cmd = "touch {0}; {1}".format(procfile,cmd)

			if not '{outfile}' in cmd:
				cmd += " | tee {outfile} "
			cmd = cmd.replace("{host}","{0}").replace("{port}","{1}").replace("{outfile}","{2}").format(host,port,outfile)
			cmd += getFinishedCmd(host=host, scan_name=scan_name, port=port)
		
			cmd += "rm {0}; ".format(procfile)

			return cmd

def getFinishedCmd(scan_name='Unknown', host='Unknown', port=None):
	cmd = "; echo '{2}{0} Scan on {1}".format(scan_name,host, color.important_color)
	if(not port is None):
		cmd += ":" + str(port)
	cmd += " complete{0}';".format(color.neutral)
	return cmd

#internal use, don't bother using
def _ScanHost(args):
	ScanHost(args[0],args[1],args[2],args[3],args[4],args[5])

def ScanHost(name, host, action, valid_services = [], valid_ports = [], run_once=False):
	print("starting scan: " + name + " - " + host)

	has_run=False

	hpath = fileutil.getPortPath(host,None)
	if debug: print("using path: " + hpath)

	if debug: print("Attempting {0} on {1}".format(name,host))
	if debug: print("valid_services: " + str(valid_services))
	if debug: print("valid_ports: " + str(valid_ports))

	if len(valid_services) + len(valid_ports) > 0:
		for portdir in fileutil.getSubDirs(hpath):
			#run once check
			if not run_once or not has_run:
				portdir = os.path.join(hpath,portdir)
				portinfo = portdir.split('/')[-1].split('.')

				port = portinfo[1]
				proto = portinfo[2]
				if debug: print("PORTINFO" + str(portinfo))
				if debug: print("CHECKING {0}/{1}".format(port,proto))

				#is in desired services check
				if(proto in valid_services or port in valid_ports):
					has_run=True

					filepath = os.path.join(portdir, name + '.scan.txt')
					if run_once: #I don't want to have to look too hard for these
						filepath = os.path.join(hpath, name + '.scan.txt')

					cmd = parseCommand(cmd=action, scan_name=name, host=host, port=port, outfile=filepath)

					if debug: print(cmd)
					shell_exec(cmd)
				

	else: #host level scan
		has_run=True
		filepath =  os.path.join(hpath, name + '.scan.txt')

		cmd = parseCommand(cmd=action, scan_name=name, host=host, port=None, outfile=filepath)

		print(cmd)
		shell_exec(cmd)
	if not has_run:
		print("SKIPPING {0} SCAN".format(name))

#not sure how to pickle keywords
def shell_exec(cmd):
	subprocess.call(cmd, shell=True)




class GenericScanner:
	def __init__(self):
		self.Pool = Pool()
	def __del__(self):
		self.Pool.close()

	#sa_lock = Lock()
	def ScanAll(self, name, action, valid_services = [], valid_ports = [], run_once=False, ip_range=None):
		ips= nmap_parser.parseIpRange(ip_range)

		#sa_lock.acquire()
		try:
			map_args = []
			for host in fileutil.getSubDirs(fileutil.getPortPath(None,None)):
				if not ip_range or host in ips:
					print("Running cmd on all hosts: " + action)
					map_args.append([name, host, action, valid_services, valid_ports, run_once])

			self.Pool.apply_async(_ScanHost, map_args)
		finally:
			pass
			#sa_lock.release()

	#internal use, don't bother using
	def _ScanHost(self, args):
		ScanHost(args[0],args[1],args[2],args[3],args[4],args[5])

	def ScanHost(self, name, host, action, valid_services = [], valid_ports = [], run_once=False):
		ScanHost(name, host, action, valid_services = [], valid_ports = [], run_once=False)
