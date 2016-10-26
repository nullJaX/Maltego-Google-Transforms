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
	value = ""
	if 'nickname' in person:
		value = person['nickname']
	else:
		value = person['displayName']
		
	m = me.addEntity("nullJaX.GooglePlusPeopleResource",value)
	m.setType("nullJaX.GooglePlusPeopleResource")
	m.setValue(person['url'])
	m.setDisplayInformation(person['url'])
	m.setIconURL(person['image']['url'])
		
	#add all fields - TODO
	m.addAdditionalFields("UID","UID",True,person['id'])
	m.addAdditionalFields("displayName","Display Name",True,person['displayName'])

	if 'givenName' in person:
		m.addAdditionalFields("givenName","First Name",True,person['name']['givenName'])
	if 'middleName' in person:
		m.addAdditionalFields("middleName","Middle Name",True,person['name']['middleName'])
	if 'familyName' in person:
		m.addAdditionalFields("familyName","Surname",True,person['name']['familyName'])
	if 'honorificPrefix' in person:
		m.addAdditionalFields("honorificPrefix","Honorific Prefix",True,person['name']['honorificPrefix'])
	if 'honorificSuffix' in person:
		m.addAdditionalFields("honorificSuffix","Honorific Suffix",True,person['name']['honorificSuffix'])
	if 'birthday' in person:
		m.addAdditionalFields("birthday","Date of birth",True,person['birthday'])
	if 'gender' in person:
		m.addAdditionalFields("gender","Gender",True,person['gender'])
	if 'url' in person:
		m.addAdditionalFields("url","Profile URL",True,person['url'])
	if 'aboutMe' in person:
		m.addAdditionalFields("aboutMe","Biography",True,person['aboutMe'])
	if 'relationshipStatus' in person:
		relationshipStatus = person['relationshipStatus'].replace("_"," ")
		m.addAdditionalFields("relationshipStatus","Relationship Status",True,relationshipStatus)
	if 'ageRange' in person:
		age_range = person['ageRange']['min'].encode('utf-8')+" "+person['ageRange']['max']
		m.addAdditionalFields("ageRange","Age Range",True,age_range)
	if 'emails' in person:
		emails = ""
		for email in person['emails']:
			emails += "("+email['type']+") "+email['value']+"; "
		m.addAdditionalFields("emails","Emails",True,emails)
	if 'occupation' in person:
		m.addAdditionalFields("occupation","Occupation",True,person['occupation'])
	if 'skills' in person:
		m.addAdditionalFields("skills","Skills",True,person['skills'])
	if 'urls' in person:
		urls = ""
		for url in person['urls']:
			urls += "("+url['label']+":"+url['type']+") "+url['value']+"; "
		m.addAdditionalFields("urls","URLs related",True,urls)

	#add note with organizations details - TODO
	if 'organizations' in person:
		organizations = ""
		for organization in person['organizations']:
			organizations += organization['name']+"; "
		m.addAdditionalFields("organizations","Organizations",True,organizations)

	if 'placesLived' in person:
		places = ""
		for place in person['placesLived']:
			if 'primary' in place:
				places += "(primary residence) "
			places += place['value']+"; "
		m.addAdditionalFields("placesLived","Places",True,places)

	me.heartbeat()
	me.returnOutput()
except:
	me.addException("Something went wrong :(")
	me.throwExceptions()