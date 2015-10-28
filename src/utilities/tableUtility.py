# output analyzer
# Currently the outputs are firstTable and secondTable
# First table is easy to access by id
# second table is not.

def getFromSecondTable(idNum,secondTable):
	outputList = [];
	for rule in secondTable.values():
		if rule['id'] == idNum:
			outputList.append(rule);
	return outputList;
