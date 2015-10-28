'''
timeSlotProcess.py

My original implementation of timeslots invovled discrete time slots
with True or False.
This won't work for the current implementation without some changes.
The main reason being that we are now organized by location. As such,
each location can have multiple regulations. Some regulations will 
allow for parking, some will forbid it.

What we can do is a bit of processing when creating our time slots.
For each location
	for each time slot
		time slot = true
		for each rule
			if rule is no parking
				time slot = false
				break

We also have to comsider how we're going to display this data.
If we have it in geojson, it might be easy to throw it up with 
with an off the shelf solution.

Leaflet?
	open source
	everything is private
	cons - implement data hosting server
ESRI?
	don't need to publicize data?
Google Fusion Tables?
	advantage - have working example
Carto DB?

'''

def getTimeSlotList():
	timeSlots = [
			'00:00','00:15','00:30','00:45',
			'01:00','01:15','01:30','01:45',
			'02:00','02:15','02:30','02:45',
			'03:00','03:15','03:30','03:45',
			'04:00','04:15','04:30','04:45',
			'05:00','05:15','05:30','05:45',
			'06:00','06:15','06:30','06:45',
			'07:00','07:15','07:30','07:45',
			'08:00','08:15','08:30','08:45',
			'09:00','09:15','09:30','09:45',
			'10:00','10:15','10:30','10:45',
			'11:00','11:15','11:30','11:45',
			'12:00','12:15','12:30','12:45',
			'13:00','13:15','13:30','13:45',
			'14:00','14:15','14:30','14:45',
			'15:00','15:15','15:30','15:45',
			'16:00','16:15','16:30','16:45',
			'17:00','17:15','17:30','17:45',
			'18:00','18:15','18:30','18:45',
			'19:00','19:15','19:30','19:45',
			'20:00','20:15','20:30','20:45',
			'21:00','21:15','21:30','21:45',
			'22:00','22:15','22:30','22:45',
			'23:00','23:15','23:30','23:45'
			]
	return timeSlots;

from dateutil.parser import *;
from dateutil.relativedelta import *;
from datetime import *;

# Specific handling of expected text with "midnight" in it.
def isMidnight(text):
	if text.strip().lower() == "12:00 MIDNIGHT".lower():
		return True;
	return False;

# Use when comparing to end time
def isBefore(current,end):
	if end.strip() == "" or current.strip() == "":
		return False;
	currentp = parse(current);
	endp = parse(end);
	delta = relativedelta(currentp,endp);
	if delta.hours <= 0 and delta.minutes <= 0 and delta.seconds <= 0:
		return True;
	return False;

# Use when comparing to start time
def isAfter(current,start):
	if start.strip() == "" or current.strip() == "":
		return False;
	currentp = parse(current);
	startp = parse(start);
	delta = relativedelta(currentp,startp);
	if delta.hours >= 0 and delta.minutes >= 0 and delta.seconds >= 0:
		return True;
	return False;

def timeSlotInRange(timeSlot,timeRange):
	if timeRange.strip() == "":
		return True;
	# Get start and end time, separated by '-'
	start = "12:00 AM";
	end = "11:59 PM";
	split = timeRange.split('-');
	if not (len(split) == 2):
		print "Error - timeRange not length 2: "+str(timeRange)+".";
	else:
		start = split[0].strip();
		end = split[1].strip();

	# This dateutil parser can't parse "12:00 MIDNIGHT".
	# Handle manually
	if isMidnight(start):
		start = "12:00 AM";
	if isMidnight(end):
		end = "12:00 AM";

	try:
		if isBefore(timeSlot,end) and isAfter(timeSlot,start):
			return True;
	except:
		print "Exception in timeSlotInRange."
		print "start:" +str(start);
		print "end:" +str(end);
		print "timeSlot: "+str(timeSlot);
		print "timeRange: "+str(timeRange);
		raise;
	return False;

def addTimeSlots(locations):
	timeSlots = getTimeSlotList();
	counter = 0;
	for key,value in locations.iteritems():
		#print "In addTimeSlots: "+str(counter);
		counter = counter + 1;
		for rule in value['rules']:
			for timeSlot in timeSlots:
				rule[timeSlot] = 'True';
				if (rule['noparking'] == 'True' or 
					rule['nostopping'] == 'True'):
					if timeSlotInRange(timeSlot,rule['times']):
						rule[timeSlot] = 'False';

# returns time in a integer
# 12am = 0000
# 9am = 900
#	note the double 0
# 1:45pm = 1345
def getTimeInInt(timeString):
	if isMidnight(timeString):
		return 0;
	try:
		timep = parse(timeString);
	except:
		print "Error in getTimeInInt.";
		print "timeString: "+str(timeString);
		raise;
	hourString = str(timep.hour);
	minuteString = str(timep.minute);
	if len(minuteString) == 1:
		minuteString = "0"+minuteString;
	return int(hourString+minuteString);


def getStartEndTimes(times):
	times = times.strip();
	if times == "":
		return ('12:00 AM','11:59 PM');
	timesSplit = times.split('-');
	return (timesSplit[0],timesSplit[1]);

def addStartEnd(locations):
	for latlong,values in locations.iteritems():
		for rule in values['rules']:
			(startTime,endTime) = getStartEndTimes(rule['times']);
			rule['start'] = startTime;
			rule['end'] = endTime;

# I can't figure out how to store these non-flat data structures into 
# Google Fusion Tables. So, I'm going to flatten everything.
# Thats 24 hours x 4 minute segments x 7 days = 672 extra columns!
def getDaysList():
	myList = ['sun','mon','tues','wed','thurs','fri','sat'];
	return myList;

def flatten(locations):
	days = getDaysList();
	timeSlots = getTimeSlotList();

	#counter = 0;
	for latlong,location in locations.iteritems():
		#print "In flatten: "+str(counter);
		#counter = counter + 1;
		for day in days:
			for timeSlot in timeSlots:
				fieldName = day+timeSlot;
				location[fieldName] = 'True';
				for rule in location['rules']:
					if rule[day] == 'True' and rule[timeSlot] == 'False':
						location[fieldName] = 'False';

def run(locations):
	addTimeSlots(locations);
	flatten(locations);

# Create two separate structures, which will be turned into two tables.
# firstTable contains all points (locations)
# secondTable contains all rules. This table has more entries than firstTable.
# 
def runTwoTables(locations):
	addStartEnd(locations);

	firstTable = {};
	secondTable = {};
	for (latitude,longitude),values in locations.iteritems():
		index = values['id'];
		firstTable[index] = {};
		firstTable[index]['id'] = index;
		firstTable[index]['latitude'] = latitude;
		firstTable[index]['longitude'] = longitude;
		firstTable[index]['rules'] = "";
		firstTable[index]['time1'] = values['time1'];
		firstTable[index]['time2'] = values['time2'];
		firstTable[index]['day1'] = values['day1'];
		firstTable[index]['day2'] = values['day2'];


	index = 0;
	for (latitude,longitude),values in locations.iteritems():
		locationID = values['id'];
		for rule in values['rules']:
			firstTable[locationID]['rules'] = (
				firstTable[locationID]['rules'] + 
				"; " + rule['description']);

			secondTable[index] = {};
			secondTable[index]['id'] = locationID;
			secondTable[index]['sun'] = rule['sun'];
			secondTable[index]['mon'] = rule['mon'];
			secondTable[index]['tues'] = rule['tues'];
			secondTable[index]['wed'] = rule['wed'];
			secondTable[index]['thurs'] = rule['thurs'];
			secondTable[index]['fri'] = rule['fri'];
			secondTable[index]['sat'] = rule['sat'];
			secondTable[index]['start'] = getTimeInInt(rule['start']);
			secondTable[index]['end'] = getTimeInInt(rule['end']);
			secondTable[index]['rule'] = rule['description'];
			noParking = 'False';
			if rule['noparking'] == 'True' or rule['nostopping'] == 'True':
				noParking = 'True';
			secondTable[index]['noparking'] = noParking;
			index = index + 1;
	
	return (firstTable,secondTable);


