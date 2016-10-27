import sys
import io
import json

import httplib2
import apiclient.discovery
from MaltegoTransform import *

GOOGLEPLUS_API_KEY = "AIzaSyCQUjsJBAKSLNqM187Yro9z8lFO8KUXyVE"

#initialize maltego transform and retrieve input entity value
me = MaltegoTransform()
me.parseArguments(sys.argv)
Q = me.getValue()

try:
	#initialize G+
	service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(), developerKey=GOOGLEPLUS_API_KEY)

	#get query result
	activities = service.activities().search(query=Q,maxResults=20).execute()

	for activity in activities['items']:
		value = ""
		if 'title' in activity:
			value = activity['title']
		else:
			value = activity['url']
		ent = me.addEntity("nullJaX.GooglePlusActivity",value)
		ent.setType("nullJaX.GooglePlusActivity")
		ent.setValue(value)
		if 'published' in activity:
			ent.addAdditionalFields("published","Published",True,activity['published'])
		if 'updated' in activity:
			ent.addAdditionalFields("updated","Updated",True,activity['updated'])
		ent.addAdditionalFields("AID","Activity ID",True,activity['id'])
		ent.addAdditionalFields("url","Activity URL",True,activity['url'])
		ent.addAdditionalFields("uid","Publisher UID",True,activity['actor']['id'])
		if 'geocode' in activity:
			ent.addAdditionalFields("geocode","Geocode",True,activity['geocode'])
		if 'address' in activity:
			ent.addAdditionalFields("address","Address",True,activity['address'])
		if 'radius' in activity:
			ent.addAdditionalFields("radius","Radius",True,activity['radius'])
		if 'placeName' in activity:
			ent.addAdditionalFields("placeName","Name of Place",True,activity['namePlace'])
		me.heartbeat()
		
	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()