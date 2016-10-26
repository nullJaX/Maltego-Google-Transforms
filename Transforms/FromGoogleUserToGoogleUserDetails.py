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
	m = me.addEntity("nullJaX.GooglePlusPeopleResource",person['nickname'])
	m.setType("nullJaX.GooglePlusPeopleResource")
	m.setValue(person['nickname'])
	m.setDisplayInformation(person['nickname'])
	m.setIconURL(person['image']['url'])
	
	#add all fields - TODO
	m.addAdditionalFields("UID","UID",True,person['id'])
	m.addAdditionalFields("displayName","Display Name",True,person['displayName'])
	m.addAdditionalFields("givenName","First Name",True,person['name']['givenName'])
	m.addAdditionalFields("middleName","Middle Name",True,person['name']['middleName'])
	m.addAdditionalFields("familyName","Surname",True,person['name']['familyName'])
	m.addAdditionalFields("honorificPrefix","Honorific Prefix",True,person['name']['honorificPrefix'])
	m.addAdditionalFields("honorificSuffix","Honorific Suffix",True,person['name']['honorificSuffix'])
	m.addAdditionalFields("birthday","Date of birth",True,person['birthday'])
	m.addAdditionalFields("gender","Gender",True,person['gender'])
	m.addAdditionalFields("url","Profile URL",True,person['url'])
	m.addAdditionalFields("aboutMe","Biography",True,person['aboutMe'])
	relationshipStatus = person['relationshipStatus'].replace("_"," ")
	m.addAdditionalFields("relationshipStatus","Relationship Status",True,relationshipStatus)
	age_range = person['ageRange']['min']+" "+person['ageRange']['max']
	m.addAdditionalFields("ageRange","Age Range",True,age_range)
	emails = ""
	for email in person['emails']:
		emails += "("+email['type']+") "+email['value']+"; "
	
	m.addAdditionalFields("emails","Emails",True,emails)
	m.addAdditionalFields("occupation","Occupation",True,person['occupation'])
	m.addAdditionalFields("skills","Skills",True,person['skills'])
	urls = ""
	for url in person['urls']:
		urls += "("+url['label']+":"+url['type']+") "+url['value']+"; "
		
	m.addAdditionalFields("urls","URLs related",True,urls)
	
	#add note with organizations details - TODO
	organizations = ""
	for organization in person['organizations']:
		organizations += organization['name']
	m.addAdditionalFields("organizations","Organizations",True,organizations)
	
	places = ""
	for place in person['placesLived']:
		if(place['primary']):
			places += "(primary residence) "
		places += place['value']+"; "
	m.addAdditionalFields("placesLived","Places",True,places)
	
	me.heartbeat()
	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()