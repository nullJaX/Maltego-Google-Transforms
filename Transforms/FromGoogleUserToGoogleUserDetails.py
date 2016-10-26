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
	person = service.people().get(userId=Q).execute()
	
	#basic info about entity
	m = me.addEntity('nullJaX.GooglePlusPeopleResource',person['nickname'])
	m.setType('nullJaX.GooglePlusPeopleResource')
	m.setValue(person['nickname'])
	m.setDisplayInformation(person['nickname'])
	m.setIconURL(person['image']['url'])
	
	#add all fields - TODO
	m.addAdditionalFields()

	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()