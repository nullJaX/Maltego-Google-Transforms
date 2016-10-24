import sys
import io
import json

import httplib2
import apiclient.discovery
from MaltegoTransform import *

me = MaltegoTransform()
me.parseArguments(sys.argv)
Q = me.getValue()
#debug
#Q = sys.argv[1]
API_KEY = "AIzaSyCQUjsJBAKSLNqM187Yro9z8lFO8KUXyVE"

service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(), developerKey=API_KEY)
people_feed = service.people().search(query=Q).execute()
enities = []
for person in people_feed['items']:
	preImageURL = person['image']
	imageURL = preImageURL['url']
	ent = me.addEntity("nullJaX.Affiliation-Google-Plus",person['displayName'])
	ent.setType("nullJaX.Affiliation-Google-Plus")
	ent.setValue(person['displayName'])
	ent.addAdditionalFields("UID","UID",True,person['id'])
	ent.addAdditionalFields("Profile URL","Profile URL", True, person['url'])
	ent.addAdditionalFields("Avatar URL","Avatar URL",True, imageURL)
	ent.setIconURL(imageURL)
	me.heartbeat()
	ent.returnEntity()
	#print(person['displayName']+" : "+person['id']+" : "+imageURL)
me.returnOutput()