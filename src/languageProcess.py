# languageProcess.py
import re;

# return dictionary
# sun, mon, tues, wed, thurs, fri, sat
def getValidDays(inputString):
	# If no days are specified, implies every day(?)
	if inputString.strip() == "":
		inputString = "sun mon tues wed thurs fri sat";
	days = {};
	days['sun'] = False;
	days['mon'] = False;
	days['tues'] = False;
	days['wed'] = False;
	days['thurs'] = False;
	days['fri'] = False;
	days['sat'] = False;
	for word in inputString.split():
		wordLower = word.lower();
		if wordLower == 'sun':
			days['sun'] = True;
		elif wordLower == 'mon':
			days['mon'] = True;
		elif wordLower == 'tues':
			days['tues'] = True;
		elif wordLower == 'wed':
			days['wed'] = True;
		elif wordLower == 'thurs':
			days['thurs'] = True;
		elif wordLower == 'fri':
			days['fri'] = True;
		elif wordLower == 'sat':
			days['sat'] = True;
		elif wordLower == 'mon-fri' or wordLower == 'schooldays':
			days['mon'] = True;
			days['tues'] = True;
			days['wed'] = True;
			days['thurs'] = True;
			days['fri'] = True;
		elif wordLower == 'sat-sun':
			days['sat'] = True;
			days['sun'] = True;
	return days;

def hasPhrase(phrase,inputString):
	return phrase in inputString.lower();

# Per some investigation, the no parking regulations seem to be governed by DAY1.
def addValidDays(jsonObject):
	for location in jsonObject:
		for rule in jsonObject[location]['rules']:
			days = getValidDays(rule['days']);
			rule['sun'] = 'False';
			rule['mon'] = 'False';
			rule['tues'] = 'False';
			rule['wed'] = 'False';
			rule['thurs'] = 'False';
			rule['fri'] = 'False';
			rule['sat'] = 'False';
			if days['sun'] == True:
				rule['sun'] = 'True';
			if days['mon'] == True:
				rule['mon'] = 'True';
			if days['tues'] == True:
				rule['tues'] = 'True';
			if days['wed'] == True:
				rule['wed'] = 'True';
			if days['thurs'] == True:
				rule['thurs'] = 'True';
			if days['fri'] == True:
				rule['fri'] = 'True';
			if days['sat'] == True:
				rule['sat'] = 'True';

# Looks like every time "any" is used, it is with "any time", so that's nice.
def addAnyTime(jsonObject):
	for location in jsonObject:
		for rule in jsonObject[location]['rules']:
			rule['anytime'] = 'False';
			if hasPhrase('anytime',rule['description']):
				rule['anytime'] = 'True';

def addNoParkingTypes(jsonObject):
	for location in jsonObject:
		for rule in jsonObject[location]['rules']:
			rule['noparking'] = 'False';
			if hasPhrase('no parking',rule['description']):
				rule['noparking'] = 'True';
			rule['nostopping'] = 'False';
			if hasPhrase('no stopping',rule['description']):
				rule['nostopping'] = 'True';

def run(jsonObject):
	addValidDays(jsonObject);
	addAnyTime(jsonObject);
	addNoParkingTypes(jsonObject);
	