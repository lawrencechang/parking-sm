import sqlite3
import json

def createLocationsTable(cursor):
	cursor.execute("""create table locations(
		id integer primary key,
		latitude double,
		longitude double,
		description text
		)""");

def createDaysTable(cursor):
	cursor.execute("""
		create table days(
				id integer primary key autoincrement,
				day text,
				t0000 bool, t0015 bool,	t0030 bool,	t0045 bool,
				t0100 bool, t0115 bool,	t0130 bool,	t0145 bool,
				t0200 bool, t0215 bool,	t0230 bool,	t0245 bool,
				t0300 bool, t0315 bool,	t0330 bool,	t0345 bool,
				t0400 bool, t0415 bool,	t0430 bool,	t0445 bool,
				t0500 bool, t0515 bool,	t0530 bool,	t0545 bool,
				t0600 bool, t0615 bool,	t0630 bool,	t0645 bool,
				t0700 bool, t0715 bool,	t0730 bool,	t0745 bool,
				t0800 bool, t0815 bool,	t0830 bool,	t0845 bool,
				t0900 bool, t0915 bool,	t0930 bool,	t0945 bool,
				t1000 bool, t1015 bool,	t1030 bool,	t1045 bool,
				t1100 bool, t1115 bool,	t1130 bool,	t1145 bool,
				t1200 bool, t1215 bool,	t1230 bool,	t1245 bool,
				t1300 bool, t1315 bool,	t1330 bool,	t1345 bool,
				t1400 bool, t1415 bool,	t1430 bool,	t1445 bool,
				t1500 bool, t1515 bool,	t1530 bool,	t1545 bool,
				t1600 bool, t1615 bool,	t1630 bool,	t1645 bool,
				t1700 bool, t1715 bool,	t1730 bool,	t1745 bool,
				t1800 bool, t1815 bool,	t1830 bool,	t1845 bool,
				t1900 bool, t1915 bool,	t1930 bool,	t1945 bool,
				t2000 bool, t2015 bool,	t2030 bool,	t2045 bool,
				t2100 bool, t2115 bool,	t2130 bool,	t2145 bool,
				t2200 bool, t2215 bool,	t2230 bool,	t2245 bool,
				t2300 bool, t2315 bool,	t2330 bool,	t2345 bool,
				locationid integer,
				foreign key(locationid) references locations(id)
			)
		""");

def loadLocations(cursor,jsonObj):
	# for each location in json
	#	insert into table
	for (idNum,dictionary) in jsonObj.iteritems():
		latitude = dictionary['latitude'];
		longitude = dictionary['longitude'];
		#description = dictionary['day1']+","+dictionary['time1'];
		description = dictionary['description']
		vals = [];
		vals.append(int(dictionary['id']));
		vals.append(latitude);
		vals.append(longitude);
		vals.append(description);
		cursor.execute("""insert into locations values(?,?,?,?)""",vals);

def loadDays(cursor,jsonObj):
	days = ["sun","mon","tues","wed","thurs","fri","sat"];
	minutes = ["00","15","30","45"];
	for (idNum,dictionary) in jsonObj.iteritems():
		for day in days:
			vals = [];
			vals.append(day);
			for hour in range(24):
				for minute in minutes:
					"""
					print day
					print twoChar(str(hour))
					print ":"
					print minute
					"""
					vals.append(boolFromTF(dictionary[
						day+
						twoChar(str(hour))+
						":"+
						minute]));
			vals.append(int(dictionary['id']));
			#print "length of vals is "+str(len(vals));
			cursor.execute("""insert into days values(
				NULL,
				?,
				?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
				?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
				?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
				?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
				?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
				?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
				?)""",vals);

def boolFromTF(character):
	if character == 'T':
		return True;
	elif character == 'F':
		return False;
	else:
		print "error in boolFromTF: char is - "+character;

def twoChar(text):
	if len(text) < 1 or len(text) > 2:
		print "Error in twoChar: text is - "+text;
		return "00";
	if len(text) == 1:
		return "0"+text;
	else:
		return text;

def main():
	# Load data file
	fileDir = "../../data/"
	filename = "signs_locations.json"
	jsonObj = json.load(open(fileDir+filename,'r'));

	# Create DB file
	dbfilename = "signs_locations.sqlite3";
	conn = sqlite3.connect(dbfilename);

	# Write to DB file
	c = conn.cursor();
	c.execute("drop table if exists locations");
	c.execute("drop table if exists days");

	print "Creating locations table."
	createLocationsTable(c);
	print "Creating days table."
	createDaysTable(c);

	loadLocations(c,jsonObj);
	loadDays(c,jsonObj);

	# Save
	conn.commit();

print "Loading json into sqlite3 db.";
main();
print "Done."