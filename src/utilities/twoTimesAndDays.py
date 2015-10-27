'''
twoTimesAndDays.py
Find which entries have two time segments. How will I deal with them?

At a cursory glance (sampled about 15 of the approx 1000 entries with two
times), it seems like when there are two times, the first time is what 
defines the restriction, and the second time defines which hours allow
parking for some specified amount of time.

Add functionality for double days as well
There's some weird things going on:
1. Sometimes the two entries are identical, but there are two regulations.
	This seems redundant, but isn't wrong.
2. Sometimes there are two different times, with different regulations.
	Seems good.
3. Sometimes one time is monday through thursday, and the other is friday,
	but there aren't two regulations. Perhaps just a error?
	They always seem to be of the "except by city permit" signs?
'''

import geojson;
import time;
import pprint;

def getDoubleEntries(geoJsonObject,fieldName1,fieldName2):
	start = time.time();
	mylist = [];
	for i in range(len(geoJsonObject['features'])):
		field1 = geoJsonObject['features'][i]['properties'][fieldName1];
		field2 = geoJsonObject['features'][i]['properties'][fieldName2];
		field1 = field1.replace(' ','');
		field2 = field2.replace(' ','');
		if field1 != '' and field2 != '':
			mylist.append((i,field1,field2));
	end = time.time();
	return (end-start,mylist);

dataDir = "../../data/"
geoFilename = "signs.geojson";
geoJsonObject = geojson.load(open(dataDir+geoFilename,'r'));

print "Getting entries with two time fields.";
(timeElapsed,mylist) = getDoubleEntries(geoJsonObject,'TIME1_REST','TIME2_REST');
print "["+str(timeElapsed)+ " seconds]";
print "There are "+str(len(mylist))+" entries with two times.";
pprint.pprint(mylist);

print "Getting entries with two day fields.";
(timeElapsed,mylist) = getDoubleEntries(geoJsonObject,'DAY1_RESTR','DAY2_RESTR');
print "["+str(timeElapsed)+ " seconds]";
print "There are "+str(len(mylist))+" entries with two days.";
pprint.pprint(mylist);
