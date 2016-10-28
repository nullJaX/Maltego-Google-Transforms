import sys
import io
import json

import httplib2
import apiclient.discovery
from MaltegoTransform import *

GOOGLEPLUS_API_KEY = "AIzaSyCQUjsJBAKSLNqM187Yro9z8lFO8KUXyVE"

#initialize maltego transform and retrieve input entity argument
me = MaltegoTransform()
me.parseArguments(sys.argv)
Q = me.getVar("AID")

try:
	#initialize G+
	service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(), developerKey=GOOGLEPLUS_API_KEY)

	#get query result
	#NOTE: this is the reduced amount of maximum results because my maltego client
	#was raising error of too long XML stream,
	#if you want to get more, just change it (max available: 100)
	max=15
	
	
	people_feed = service.people().listByActivity(activityId=Q,maxResults=max,collection='plusoners').execute()

	for person in people_feed['items']:
		preImageURL = person['image']
		imageURL = preImageURL['url']
		ent = me.addEntity("nullJaX.Affiliation-Google-Plus",person['id'])
		ent.setType("nullJaX.Affiliation-Google-Plus")
		ent.setValue(person['id'])
		ent.addAdditionalFields("Name","Name",True,person['displayName'])
		ent.addAdditionalFields("Profile URL","Profile URL", True, person['url'])
		ent.setIconURL(imageURL)
		ent.setDisplayInformation(person['displayName'])
		me.heartbeat()
	
	people_feed = service.people().listByActivity(activityId=Q,maxResults=max,collection='resharers').execute()

	for person in people_feed['items']:
		preImageURL = person['image']
		imageURL = preImageURL['url']
		ent = me.addEntity("nullJaX.Affiliation-Google-Plus",person['id'])
		ent.setType("nullJaX.Affiliation-Google-Plus")
		ent.setValue(person['id'])
		ent.addAdditionalFields("Name","Name",True,person['displayName'])
		ent.addAdditionalFields("Profile URL","Profile URL", True, person['url'])
		ent.setIconURL(imageURL)
		ent.setDisplayInformation(person['displayName'])
		me.heartbeat()

	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()