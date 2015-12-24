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
	import uniqueLatLong as unique;
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

def timeSlotProcessSeparate(locations):
	print "Time slot process \"separate\" step.";
	start = time.time();
	import timeSlotProcess;
	(firstTable,secondTable) = timeSlotProcess.runTwoTables(locations);
	end = time.time();
	print "["+str(end-start)+" seconds]";
	return (firstTable,secondTable);

# Not a good function?? Changes input var, instead of returning new var?
def timeSlotProcessSingle(locations):
	print "Time slot process \"single\" step.";
	start = time.time();
	import timeSlotProcess;
	#flattened = timeSlotProcess.runFlatten(locations);
	flattened = timeSlotProcess.runFlattenSmall(locations);
	end = time.time();
	print "["+str(end-start)+" seconds]";
	return flattened;

def writeCSV(dictObject,dataDir,filename):
	print "Outputting to CSV file.";
	start = time.time();
	import fileWriter;
	fileWriter.runCSV(dictObject,dataDir,filename);
	end = time.time();
	print "["+str(end-start)+" seconds]";

def writeJSON(dictObject,dataDir,filename):
	print "Outputting to JSON file.";
	start = time.time();
	import fileWriter;
	fileWriter.runJSON(dictObject,dataDir,filename);
	end = time.time();
	print "["+str(end-start)+" seconds]";

def main():
	dataDir = "../data/";
	geoJsonFilename = "signs_parking.geojson";
	t1csvFilename = "signs_parking_table1.csv";
	t2csvFilename = "signs_parking_table2.csv";
	t1jsonFilename = "signs_parking_table1.json";
	t2jsonFilename = "signs_parking_table2.json";
	flattenedFilename = "signs_locations.json";

	geoJsonObject = geojson.load(open(dataDir+geoJsonFilename,'r'));
	textProcess(geoJsonObject);
	locations = uniqueLocations(geoJsonObject);
	languageProcess(locations);
	(firstTable,secondTable) = timeSlotProcessSeparate(locations);
	flattened = timeSlotProcessSingle(locations);
	writeCSV(firstTable,dataDir,t1csvFilename);
	writeCSV(secondTable,dataDir,t2csvFilename);
	writeJSON(firstTable,dataDir,t1jsonFilename);
	writeJSON(secondTable,dataDir,t2jsonFilename);
	writeJSON(flattened,dataDir,flattenedFilename);

	return (firstTable,secondTable,flattened);

(firstTable,secondTable,flattened) = main();

# For console 
import utilities.tableUtility as tu;
import pprint;

'''
# Extra info
import pprint;
pprint.pprint(data[data.keys()[0]]);
for key in data.keys():
	if len(data[key]['rules']) > 1:
		pprint.pprint(data[key]);
		break;
'''

