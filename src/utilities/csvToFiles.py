# Write out all entries for each field in a separate file
import csv;
import time;

def writeFiles(dataDir,csvFilename):
	start = time.time();
	csvfile = open(dataDir+csvFilename, 'r');
	# "If the fieldnames parameter is omitted, the values in the first row of the csvfile will be used as the fieldnames."
	reader = csv.DictReader(csvfile);

	fields = reader.fieldnames;
	#print fields;

	# Create files for each field
	fieldFiles = [];
	for field in fields:
		fieldFiles.append(open(dataDir+field+".txt",'w'));

	data = list(reader);
	for index,field in enumerate(fields):
		currentFile = fieldFiles[index];
		#for row in iter(data):
		for row in data:
			currentFile.write(row[field]+'\n');

	for filePointer in fieldFiles:
		filePointer.close();

	end = time.time();
	return end-start;


dataDir = "../../data/"
csvFilename = "signs.csv";
print "Writing files for each field in the CSV.";
timeElapsed = writeFiles(dataDir,csvFilename);
print "["+str(timeElapsed)+ " seconds]";

