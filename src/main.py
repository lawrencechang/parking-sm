'''
main

Major funcitons
1. File conversions, formatting, field name matching
2. Text process - spelling, abbreviations, fixing known typos
2.1. Change data from using signs as the canonical representation,
	to locations.
3. Language process - Phrases, keywords, times
4. Timeslots
	
'''

import time;
import geojson;

def fileProcess(dataDir,inputFilename,outputFilename):
	start = time.time();
	end = time.time();
	print "["+str(end-start)+" seconds]";

def textProcess(geoJsonObject):
	print 'Text process step.';
	start = time.time();
	import textProcess;
	textProcess.run(geoJsonObject);
	end = time.time();
	print "["+str(end-start)+" seconds]";

# Because we aren't just modifying the structure, but replacing it,
# we can't just send it back via the same reference.
def uniqueLocations(geoJsonObject):
	print "Unique locations step.";
	start = time.time();
	import utilities.uniqueLatLong as unique;
	(timeElapsed,locations) = unique.getUniqueLocations(geoJsonObject);
	end = time.time();
	print "["+str(end-start)+" seconds]";
	return locations;

def languageProcess(locations):
	print 'Language process step.';
	start = time.time();
	import languageProcess;
	languageProcess.run(locations);
	end = time.time();
	print "["+str(end-start)+" seconds]";

def timeSlotProcess(locations):
	print "Time slot process step.";
	start = time.time();
	import timeSlotProcess;
	#timeSlotProcess.run(locations);
	(firstTable,secondTable) = timeSlotProcess.runTwoTables(locations);
	end = time.time();
	print "["+str(end-start)+" seconds]";
	return (firstTable,secondTable);

def makeCSV(locations,dataDir,filename):
	print "Making CSV for Google Fusion Tables.";
	start = time.time();
	import makeCSV;
	makeCSV.run(locations,dataDir,filename);
	end = time.time();
	print "["+str(end-start)+" seconds]";

def main():
	dataDir = "../data/";
	geoJsonFilename = "signs_parking.geojson";
	t1csvFilename = "signs_parking_table1.csv";
	t2csvFilename = "signs_parking_table2.csv";

	geoJsonObject = geojson.load(open(dataDir+geoJsonFilename,'r'));
	textProcess(geoJsonObject);
	locations = uniqueLocations(geoJsonObject);
	languageProcess(locations);
	(firstTable,secondTable) = timeSlotProcess(locations);
	makeCSV(firstTable,dataDir,t1csvFilename);
	makeCSV(secondTable,dataDir,t2csvFilename);

	return (firstTable,secondTable);
(firstTable,secondTable) = main();

'''
# Extra info
import pprint;
pprint.pprint(data[data.keys()[0]]);
for key in data.keys():
	if len(data[key]['rules']) > 1:
		pprint.pprint(data[key]);
		break;
'''

