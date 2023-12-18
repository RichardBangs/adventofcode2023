import os
import sys



def transposeArea(area : [str]) -> [str]:

	numRows = len(area)
	numCols = len(area[0])

	newArea : [str] = []

	for col in range(numCols):
		myStr = ""
		for row in range(numRows):
			myStr += area[row][col]
		
		newArea.append(myStr)
		
	return newArea




def findRef(area : [str]) -> int:

	#print(area)

	numRows = len(area)
	numCols = len(area[0])

	countErrors = 0

	# vertical
	foundRow = 0
	for row in range(0, numRows-1):

		#print(f"{area[row]}")

		isValid = True
		for index in range(0, row+1):

			diff0 = row-index
			diff1 = row+index+1

			if(diff0 < 0 or diff1 >= numRows):
				break

			#print(f"{area[diff0]} vs {area[diff1]}")

			if(area[diff0] != area[diff1]):
				isValid = False
				break

		if(isValid):
			foundRow = row+1
			break

	return foundRow


def findRef2(area : [str]) -> int:

	#print(area)

	numRows = len(area)
	numCols = len(area[0])

	# vertical
	foundRow = 0
	for row in range(0, numRows-1):

		errorCount = 0

		print(f"checking row={row} {area[row]}")

		isValid = True
		for index in range(0, row+1):

			diff0 = row-index
			diff1 = row+index+1

			if(diff0 < 0 or diff1 >= numRows):
				break

			for charIndex in range(0, len(area[diff0])):
				if(area[diff0][charIndex] != area[diff1][charIndex]):
					errorCount += 1

		print(f"	errors={errorCount}")

		if(errorCount == 1):
			foundRow = row+1
			break

	return foundRow


def main_part1(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	row = 0
	area : [str] = []
	numRows : int = len(fullInput)
	
	while(True):

		if(row < numRows):
			line = fullInput[row].strip('\n')

		if(line == "" or row >= numRows):		

			x = 0
			y = 0

			y = findRef(area)
			x = findRef(transposeArea(area))

			if(x != 0 and y != 0):
				print(f"WTF {x},{y}")

			refValue = x + (y * 100)
			print(refValue)
			sum += refValue

			area.clear()
		else:
			area.append(line)

		if(row >= numRows):
			break

		row += 1

	print(sum)

	return sum



def main_part2(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	row = 0
	area : [str] = []
	numRows : int = len(fullInput)
	
	while(True):

		if(row < numRows):
			line = fullInput[row].strip('\n')

		if(line == "" or row >= numRows):		

			y = findRef2(area)
			x = findRef2(transposeArea(area))

			if(x != 0 and y != 0):
				print(f"WTF {x},{y}")

			refValue = x + (y * 100)
			print(f"{refValue} xy={x},{y}")
			sum += refValue

			area.clear()
		else:
			area.append(line)

		if(row >= numRows):
			break

		row += 1

	print(sum)

	return sum





argPart : int = int(sys.argv[1])
argInputFile : str = sys.argv[2]

retVal = 0

if(argPart == 1):
	retVal = main_part1(argInputFile)
else:
	retVal = main_part2(argInputFile)

sys.exit(retVal)