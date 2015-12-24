'''
makeCSV.py

Turns  a JSON object into a CSV.
Heavily adopted from "jsonHelper.py" from previous codebase.

'''

def runCSV(locations,fileDir,filename):
	import csv;
	csvFile = csv.writer(open(fileDir+filename,'w'));

	# Get the fieldnames
	fieldnames = [];
	firstKeyRandom = locations.keys()[0];
	for fieldname in locations[firstKeyRandom]:
		fieldnames.append(fieldname);

	# Don't add rules to CSV
	#if 'rules' in fieldnames:
	#	fieldnames.remove('rules');

	csvFile.writerow(fieldnames);
	for key,values in locations.iteritems():
		valuesList = [];
		for fieldname in fieldnames:
			valuesList.append(values[fieldname]);
		csvFile.writerow(valuesList);

def runJSON(locations,fileDir,filename):
	import json;
	outputFile = open(fileDir+filename,'w');
	try:
		temp = json.dumps(locations);
	except:
		print "locations variable isn't json outputtable.";
		raise;
	json.dump(locations,outputFile);
