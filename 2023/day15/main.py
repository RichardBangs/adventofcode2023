import os
import sys


def hashFunc(myString : str) -> int:

	hashResult = 0


	for myChar in myString:
		hashResult += ord(myChar)
		hashResult = (hashResult*17) % 256

	return hashResult




def main_part1(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	fullString = ""

	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

		fullString += fullInput[row]

	stringList = fullString.split(',')

	hashSum = 0

	for q in stringList:
		hashSum += hashFunc(q)

	print(hashSum)

	return hashSum



def main_part2(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	fullString = ""

	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

		fullString += fullInput[row]

	stringList = fullString.split(',')

	#rn=1
	#hash(rn) -> Box
	# = -> add to box
	#	note number after
	# - -> remove from box


	# List of Hash Maps

	boxList : [{int, int}] = []

	for index in range(0, 256):
		boxList.append({})

	for q in stringList:

		if('=' in q):
			label = q.split('=')[0]
			boxList[hashFunc(label)][label] = q.split('=')[1]
		elif('-' in q):
			label = q.split('-')[0]

			if(label in boxList[hashFunc(label)]):
				boxList[hashFunc(label)].pop(label)


	focalPowerSum = 0
	for boxIndex in range(0, len(boxList)):
		for lensIndex in range(0, len(boxList[boxIndex])):
			focalPowerBox = (lensIndex + 1) * (boxIndex + 1) * int(list(boxList[boxIndex].values())[lensIndex])
			focalPowerSum += focalPowerBox

	print(focalPowerSum)

	return focalPowerSum




argPart : int = int(sys.argv[1])
argInputFile : str = sys.argv[2]

retVal = 0

if(argPart == 1):
	retVal = main_part1(argInputFile)
else:
	retVal = main_part2(argInputFile)

sys.exit(retVal)