# textProcess.py
import re;
def removeBackSlashesBetweenDaysString(inputString):
	newString = re.sub(r'\\',' ',inputString);
	return newString;

def combineSchoolDaysString(inputString):
	newString = re.sub(r'school days','schooldays',inputString);
	return newString;

def combineAnyTimeString(inputString):
	newString = re.sub(r'any time','anytime',inputString);
	return newString;	

def replaceTowAwayTripleRule(inputString):
	if inputString.lower() == "Tow-Away/No Stopping/No Parking/[Times]".lower():
		return "Tow-Away, No Stopping, No Parking, [Times]"
	return inputString;

def replaceStringsInDay(geoJsonObject):
	for i in range(len(geoJsonObject['features'])):
		currentString = geoJsonObject['features'][i]['properties']['DAY1_RESTR'];
		newString = removeBackSlashesBetweenDaysString(currentString);
		newString = combineSchoolDaysString(newString);
		geoJsonObject['features'][i]['properties']['DAY1_RESTR'] = newString;

		currentString = geoJsonObject['features'][i]['properties']['DAY2_RESTR'];
		newString = removeBackSlashesBetweenDaysString(currentString);
		newString = combineSchoolDaysString(newString);
		geoJsonObject['features'][i]['properties']['DAY2_RESTR'] = newString;

def replaceStringsInDescription(geoJsonObject):
	for i in range(len(geoJsonObject['features'])):
		currentString = geoJsonObject['features'][i]['properties']['LIB__DESCR'];
		newString = combineAnyTimeString(currentString);
		newString = replaceTowAwayTripleRule(newString);
		geoJsonObject['features'][i]['properties']['LIB__DESCR'] = newString;

def replaceKnownTypos(geoJsonObject):
	for feature in geoJsonObject['features']:
		# TIME1
		# Not a "no parking" sign.
		if feature['properties']['TIME1_REST'] == "8:00 AM - 110:00 AM":
			feature['properties']['TIME1_REST'] = "8:00 AM - 11:00 AM";
			print "Fixed typo 1.";
		# TIME2
		if feature['properties']['TIME2_REST'] == "9:00 AM - 6:00: Pr":
			feature['properties']['TIME2_REST'] = "9:00 AM - 6:00 PM";
			print "Fixed typo 2.";

def run(geoJsonObject):
	replaceKnownTypos(geoJsonObject);
	replaceStringsInDay(geoJsonObject);
	replaceStringsInDescription(geoJsonObject);