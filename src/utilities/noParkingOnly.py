'''
noParkingOnly.py

Writes a geojson file that contains only the "no parking" and "no stopping" signs.
'''

import geojson;
import time;

def getNoParkingOnly(geoJsonObject):
	start = time.time();
	features = [];
	for feature in geoJsonObject['features']:
		description = feature['properties']['LIB__DESCR'];
		if ('no parking' in description.lower() or
			'no stopping' in description.lower()):
			features.append(feature);
	end = time.time();
	return (end-start,geojson.FeatureCollection(features));

print "Creating a new geojson object with only \"no parking\" signs.";
dataDir = "../../data/"
geoFilename = "signs.geojson";
outputFilename = "signs_parking.geojson";
geoJsonObject = geojson.load(open(dataDir+geoFilename,'r'));
(timeElapsed,newJsonObject) = getNoParkingOnly(geoJsonObject);
geojson.dump(newJsonObject,open(dataDir+outputFilename,'w'));
print "["+str(timeElapsed)+ " seconds]";
