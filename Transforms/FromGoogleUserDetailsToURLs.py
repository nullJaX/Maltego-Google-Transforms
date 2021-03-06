import sys
import io
import json

import httplib2
import apiclient.discovery
from MaltegoTransform import *

GOOGLEPLUS_API_KEY = "AIzaSyCQUjsJBAKSLNqM187Yro9z8lFO8KUXyVE"

me = MaltegoTransform()
me.parseArguments(sys.argv)
Q = me.getVar('UID')

try:
	#initialize G+
	service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(), developerKey=GOOGLEPLUS_API_KEY)

	#get query result
	urls = service.people().get(userId=Q, fields='urls').execute()
	for u in urls['urls']:
		fullname = ""
		if 'type' in u:
			fullname += u['type'] + " @ "
		fullname += u['label']
		url = me.addEntity("maltego.URL",fullname)
		url.setType("maltego.URL")
		url.setValue(fullname)
		url.addAdditionalFields("url","URL",True,u['value'])
	me.heartbeat()
	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()