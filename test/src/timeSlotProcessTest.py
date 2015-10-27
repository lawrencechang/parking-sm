import os;
import sys;
sys.path.append(os.path.expanduser('~')+"/Documents/ucla/parking-sm/src/");

import unittest;
import timeSlotProcess;
import collections;

class timeSlotProcessTests(unittest.TestCase):
	def defaultTest(self):
		self.assertTrue(True);

	def testIsBefore(self):
		TimeTimeResult = collections.namedtuple('TimeTimeResult', 'endTime current result');
		testList = [
			TimeTimeResult('','00:00',False),
			TimeTimeResult('00:00','',False),
			TimeTimeResult('00:00','00:00',True),
			TimeTimeResult('00:00','00:01',False),
			TimeTimeResult('00:01','00:00',True),
			TimeTimeResult('00:59','00:58',True),
			TimeTimeResult('01:00','00:59',True),
			TimeTimeResult('00:59','01:00',False),
			TimeTimeResult('00:59','01:01',False),
			TimeTimeResult('01:59','01:59',True),
			TimeTimeResult('02:00','01:58',True),
			TimeTimeResult('23:59','00:00',True),
			TimeTimeResult('23:59','22:59',True),
			TimeTimeResult('23:58','23:59',False),
			TimeTimeResult('22:59','22:59',True),
			TimeTimeResult('12:59','13:00',False),
			TimeTimeResult('01:00','12:59',False)
		];
		for entry in testList:
			endTime = entry.endTime;
			current = entry.current;
			result = entry.result;
			try:
				self.assertEqual(timeSlotProcess.isBefore(current,endTime),result);
			except AssertionError:
				print "";
				print "current: "+entry.current;
				print "endTime: "+entry.endTime;
				print "result: "+str(entry.result);
				raise;

	def testIsAfter(self):
		TimeTimeResult = collections.namedtuple('TimeTimeResult', 'startTime current result');
		testList = [
			TimeTimeResult('','00:00',False),
			TimeTimeResult('00:00','',False),
			TimeTimeResult('00:00','00:00',True),
			TimeTimeResult('00:00','00:01',True),
			TimeTimeResult('00:01','00:00',False),
			TimeTimeResult('00:59','00:58',False),
			TimeTimeResult('01:00','00:59',False),
			TimeTimeResult('00:59','01:00',True),
			TimeTimeResult('00:59','01:01',True),
			TimeTimeResult('01:59','01:59',True),
			TimeTimeResult('02:00','01:58',False),
			TimeTimeResult('23:59','00:00',False),
			TimeTimeResult('23:59','22:59',False),
			TimeTimeResult('23:58','23:59',True),
			TimeTimeResult('22:59','22:59',True)
		];
		for entry in testList:
			startTime = entry.startTime;
			current = entry.current;
			result = entry.result;
			try:
				self.assertEqual(timeSlotProcess.isAfter(current,startTime),result);
			except AssertionError:
				print "current: "+entry.current;
				print "startTime: "+entry.startTime;
				print "result: "+str(entry.result);
				raise;

def getSuite():
	return unittest.TestLoader().loadTestsFromTestCase(timeSlotProcessTests);

#unittest.main();