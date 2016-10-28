import sys
from MaltegoTransform import *

me = MaltegoTransform()
me.parseArguments(sys.argv)

urlField = me.getVar('urls')
urlString = urlField.encode('utf-8')
urlField = urlField.replace(" ","")
urlList = urlField.split(";")
for id in range(0, len(urlList)-1):
	info = urlList[id].split(")")[0]+")"
	value = urlList[id].split(")")[1]
	url = me.addEntity("maltego.URL",info)
	url.setType("maltego.URL")
	url.setValue(info)
	url.addAdditionalFields("url","URL",True,value)
me.returnOutput()