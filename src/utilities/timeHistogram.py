# Get statistics on the type of "words" in the TIME fields
# Hypothesis - there are about 30 unique phrases only.
import time;
import pprint;

def getExpectedWordsList():
	return ['-',
			'am',
			'pm',
			'noon',
			'midnight',
			'1:00',
			'2:00',
			'3:00',
			'4:00',
			'5:00',
			'6:00',
			'7:00',
			'8:00',
			'9:00',
			'10:00',
			'11:00',
			'12:00',
			'1:30',
			'2:30',
			'3:30',
			'4:30',
			'5:30',
			'6:30',
			'7:30',
			'8:30',
			'9:30',
			'10:30',
			'11:30',
			'12:30',
			];

def getHistogram(listOfTimes):
	hist = {};
	for line in listOfTimes:
		for word in line.split():
			if word in hist:
				hist[word] = hist[word] + 1;
			else:
				hist[word] = 1;
	return hist;

def printHistogramFromFile(dir,filename):
	start = time.time();
	hist = getHistogram(open(dir+filename,'r'));
	print "Histogram: "+str(len(hist))+" unique entries.";
	pprint.pprint(hist);
	end = time.time();
	return end-start;

dataDir = "../../data/"
time1Filename = "TIME1_REST.txt";
time2Filename = "TIME2_REST.txt";
print "Getting statistics on the words in the time fields.";

print "Histogram 1 - "+time1Filename;
timeElapsed = printHistogramFromFile(dataDir,time1Filename);
print "["+str(timeElapsed)+ " seconds]";

print "Histogram 2 - "+time2Filename;
timeElapsed = printHistogramFromFile(dataDir,time2Filename);
print "["+str(timeElapsed)+ " seconds]";