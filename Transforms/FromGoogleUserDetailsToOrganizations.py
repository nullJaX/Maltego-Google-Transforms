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
	organizations = service.people().get(userId=Q, fields='organizations').execute()
	for o in organizations['organizations']:
		fullname = ""
		if 'department' in o:
			fullname += o['department'] + "@"
		fullname += o['name']
		org = me.addEntity("maltego.Organization",fullname)
		org.setType("maltego.Organization")
		org.setValue(fullname)
		note = ""
		if 'title' in o:
			note += "Title: "+o['title']+"\n"
		if 'type' in o:
			note += "Type of organization: "+o['type']+"\n"
		if 'startDate' in o:
			note += "Start date: "+o['startDate']+"\n"
		if 'endDate' in o:
			note += "End date: "+o['endDate']+"\n"
		if 'location' in o:
			note += "Location: "+o['location']+"\n"
		if 'primary' in o:
			note += "Is it primary organization? "
			if o['primary']:
				note += "Yes\n"
			else:
				note += "No\n"
		if 'description' in o:
			note += "Description:\n"+o['description']
		org.setNote(note)
	me.heartbeat()
	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()