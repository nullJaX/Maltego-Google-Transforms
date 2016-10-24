import sys
import io
import json

import httplib2
import apiclient.discovery
from MaltegoTransform import *

#initialize maltego transform and retrieve input entity value
me = MaltegoTransform()
me.parseArguments(sys.argv)
Q = me.getValue()
API_KEY = "AIzaSyCQUjsJBAKSLNqM187Yro9z8lFO8KUXyVE"

#initialize G+
service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(), developerKey=API_KEY)

#get query result
people_feed = service.people().search(query=Q).execute()


for person in people_feed['items']:
	preImageURL = person['image']
	imageURL = preImageURL['url']
	ent = me.addEntity("nullJaX.Affiliation-Google-Plus",person['id'])
	ent.setType("nullJaX.Affiliation-Google-Plus")
	ent.setValue(person['id'])
	ent.addAdditionalFields("Name","Name",True,person['displayName'])
	ent.addAdditionalFields("Profile URL","Profile URL", True, person['url'])
	ent.setIconURL(imageURL)
	me.heartbeat()
	#print(person['displayName']+" : "+person['id']+" : "+imageURL)
me.returnOutput()

#TODO: add try/except clause to provide better UX :)