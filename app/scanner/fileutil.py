import os
import xml.etree.ElementTree as ET
import json
import xml.dom.minidom as minidom

root = os.getcwd();
def getRootPath():
	return root
def getOutPath():
	return getRootPath() + '/out/'
def getTmpPath():
	return getRootPath() + '/tmp/'
def getConfigPath():
	return getRootPath() + '/etc/'

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
