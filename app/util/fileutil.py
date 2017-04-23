import os
import xml.etree.ElementTree as ET
import json
import xml.dom.minidom as minidom





def ensurePathSlash(path):
	if not path.endswith('/'):
		path = path + '/'
	return path

root = os.getcwd();
def getRootPath():
	return ensurePathSlash(root)
def getOutPath():
	return ensurePathSlash(os.path.join(getRootPath(),'out'))
def getTmpPath():
	return ensurePathSlash(os.path.join(getRootPath(), 'tmp'))
def getConfigPath():
	return ensurePathSlash(os.path.join(getRootPath(), 'etc'))
def getProgressPath():
	return ensurePathSlash(os.path.join(getTmpPath(), 'progress'))
def getSavePath():
	return ensurePathSlash(os.path.join(getRootPath(), 'saved'))
	

print 'USING ROOT PATH:'
print getRootPath()

#create directory, if not exists
def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def writeTo(path, content):
	with open(path,'w') as f:
		f.write(content)

def writeXMLTo(path, xmlNode):
	tree = ET.ElementTree(xmlNode)
	#tree.write(path)
	content = minidom.parseString(ET.tostring(xmlNode)).toprettyxml(indent="	")
	writeTo(path, content)

def writeJSONTo(path, jsonObj):
	writeTo(path, json.dumps(jsonObj, indent=4, separators=(',',': '), sort_keys=True))

def read(path):
	if not os.path.exists(path):
		return ""

	with open(path,'r') as f:
		return f.read()

def readAsJSON(path):
	try:
		return json.loads(read(path))
	except ValueError:
		return {}

def getPortPath(host,port):
	path = getOutPath()

	if not path.endswith('/'):
		path += '/'
	if not host is None:
		path += host + '/'
	if not port is None:
		path += port + '/'

	return path

def getSubDirs(path):
	return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
