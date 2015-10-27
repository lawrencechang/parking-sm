import unittest;

import timeSlotProcessTest;

def runAllTests():
	testSuite = unittest.TestSuite([
		timeSlotProcessTest.getSuite()
	]);
	unittest.TextTestRunner(verbosity=2).run(testSuite);

#if __name__ == '__main__':
runAllTests();