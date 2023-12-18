import os
import sys


def main_part1(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

	return sum



def main_part2(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

	return sum




argPart : int = int(sys.argv[1])
argInputFile : str = sys.argv[2]

retVal = 0

if(argPart == 1):
	retVal = main_part1(argInputFile)
else:
	retVal = main_part2(argInputFile)

sys.exit(retVal)