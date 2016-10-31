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
	places = service.people().get(userId=Q, fields='placesLived').execute()
	for place in places['placesLived']:
		p = me.addEntity("maltego.City",place['value'])
		if 'primary' in place:
			if place['primary']:
				p.setNote("This is a primary place.")
	me.heartbeat()
	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()