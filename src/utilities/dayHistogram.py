# dayHistogram.py
# Same functionality as timeHistogram, but for days of the week

import time;
import pprint;
import re;

def getExpectedList():
	# discovered - mon-fri, other, sat-sun
	return ['sun','mon','tues','wed','thurs','fri','sat','school days'];

def getHistogram(listOfDays):
	hist = {};
	for line in listOfDays:
		# Use regex to replace backslash with space. Just easier.
		# use the backslash \ as the delimiter
		lineClean = re.sub(r'\\',' ',line);
		for day in lineClean.split():
			if day in hist:
				hist[day] = hist[day] + 1;
			else:
				hist[day] = 1;
	return hist;

def printHistogramFromFile(dir,filename):
	start = time.time();
	hist = getHistogram(open(dir+filename,'r'));
	print "Histogram: "+str(len(hist))+" unique entries.";
	pprint.pprint(hist);
	end = time.time();
	return end-start;

dataDir = "../../data/";
day1Filename = "DAY1_RESTR.txt";
day2Filename = "DAY2_RESTR.txt";
print "Getting statistics on the words in the day fields.";

print "Histogram 1.";
timeElapsed = printHistogramFromFile(dataDir,day1Filename);
print "["+str(timeElapsed)+ " seconds]";

print "Histogram 2.";
timeElapsed = printHistogramFromFile(dataDir,day2Filename);
print "["+str(timeElapsed)+ " seconds]";