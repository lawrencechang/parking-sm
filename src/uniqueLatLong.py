'''
uniqueLatLong.py

Utility to process multiple signs exist at the same "location".
Location in quotes because even if signs are colocated, there is no
guarantee that the data conveys that with identical lat long values.

To mitigate this, perhaps use a 10 foot radius as our
cluster size of a location. That is, if two signs are within 10 feet
of each other, they are considered colocated. Why 10 feet?

1. 10 feet seems like more than enough wiggle room in terms of data
entry of lat long coordinates.
2. I don't expect street signs to be closer than 10 feet from each
other. A standard street parking space is surely longer than 10 feet.

Caveats:
1. How do I deal with a sign that is within the radius of two separate
signs?
2. How do I get these clusters?
3. What if in a series of signs, each pair of signs is within 10 feet.
So from sign 1 to sign 2, 8 feet. But from sign 2 to sign 3, 7 feet.
And from sign 1 to sign 3, 15 feet. How do we deal with this?
'''

import geojson;
import time;

# Takes a single sign and outputs up to two unique rules
# Some signs have a "no parking" element, then a # of hours
# parking rule. 
# Seems like any "double description" 
def getRulesList(objectid,description,day1,day2,time1,time2):
	# Clean any potential white space
	day1 = day1.strip();
	day2 = day2.strip();
	time1 = time1.strip();
	time2 = time2.strip();

	rules = [];
	rule1 = {};

	# Special case:
	if description.lower() == "Tow-Away/No Stopping/No Parking/[Times]".lower():
		print "We matched on first one.";
	if description.lower() == "Tow-Away\/No Stopping\/No Parking\/[Times]".lower():
		print "We matched on the second one.";

	descriptions = description.split('/');

	rule1['objectid'] = objectid;
	rule1['description'] = descriptions[0];
	rule1['days'] = day1;
	rule1['times'] = time1;
	rules.append(rule1);

	rule2 = {};
	rule2['objectid'] = objectid;

	if (not (day2 == "")) or (not (time2 == "")):
		if len(descriptions) == 1:
			rule2['description'] = descriptions[0];
			rule2['days'] = day2;
			rule2['times'] = time2;
			rules.append(rule2);
		elif len(descriptions) == 2:
			rule2['description'] = descriptions[1];
			rule2['days'] = day2;
			rule2['times'] = time2;
			rules.append(rule2);
		else:
			print "Error - more than 2 rules found!";
			print description;

	else:
		if len(descriptions) == 1:
			pass;
		elif len(descriptions) == 2:
			rule2['description'] = descriptions[1];
			rule2['days'] = day2;
			rule2['times'] = time2;
			rules.append(rule2);
		else:
			print "Error - more than 2 rules found!";
			print description;
	return rules;

def getUniqueLocations(geoJsonObject):
	start = time.time();
	locations = {};
	counter = 1;
	for feature in geoJsonObject['features']:
		objectid = feature['properties']['OBJECTID'];
		description = feature['properties']['LIB__DESCR'];
		day1 = feature['properties']['DAY1_RESTR'];
		day2 = feature['properties']['DAY2_RESTR'];
		time1 = feature['properties']['TIME1_REST'];
		time2 = feature['properties']['TIME2_REST'];
		rules = getRulesList(objectid,description,day1,day2,time1,time2);

		latitude = feature['properties']['LATITUDE'];
		longitude = feature['properties']['LONGITUDE'];
		myTuple = (latitude,longitude)
		if myTuple in locations:
			locations[myTuple]['rules'] = locations[myTuple]['rules']+rules;
		else:
			locations[myTuple] = {};
			locations[myTuple]['id'] = counter;
			locations[myTuple]['rules'] = rules;
			locations[myTuple]['latitude'] = latitude;
			locations[myTuple]['longitude'] = longitude;
			locations[myTuple]['time1'] = time1;
			locations[myTuple]['time2'] = time2;
			locations[myTuple]['day1'] = day1;
			locations[myTuple]['day2'] = day2;
			counter = counter + 1;

	end = time.time();
	return (end-start,locations);

def run():
	dataDir = "../../data/"
	geoFilename = "signs_parking.geojson";
	geoJsonObject = geojson.load(open(dataDir+geoFilename,'r'));

	print "Getting statistics on unique locations.";
	(timeElapsed,locations) = getUniqueLocations(geoJsonObject);
	print "["+str(timeElapsed)+ " seconds]";
	print "There are "+str(len(locations))+" unique locations.";
	print "(out of "+str(len(geoJsonObject['features']))+" possible.)";

	locations1 = [x for x in locations.keys() if len(locations[x]['rules']) == 1]
	locations2 = [x for x in locations.keys() if len(locations[x]['rules']) == 2]
	locations3 = [x for x in locations.keys() if len(locations[x]['rules']) == 3]
	locations4 = [x for x in locations.keys() if len(locations[x]['rules']) == 4]
	locations5 = [x for x in locations.keys() if len(locations[x]['rules']) > 4]
	return locations;

