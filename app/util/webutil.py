import os

def getLocalHostName():
	return "10.11.0.94"

def getWebUrl():
	return "http://{0}/prophet/".format(getLocalHostName())
