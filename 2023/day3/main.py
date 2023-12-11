import os
import numpy as np



def main():

	f = open("input.txt", "r")

	sum = 0

	fullInput = f.readlines();

	# Strip out new lines.
	for index in range(len(fullInput)):
		fullInput[index] = fullInput[index].strip('\n')

	print(fullInput)

	numRows = len(fullInput)
	numCols = len(fullInput[0])

	for y in range(numRows):
		
		x = 0

		while(x < numCols):

			numberString = extractNumber(fullInput, x, y, numCols)

			if (numberString != ""):

				print("Found Number = " + str(numberString))

				foundAdjacentSymbol = False

				for ix in range(len(numberString)):
					foundAdjacentSymbol |= isAdjacentToSymbol(fullInput, x+ix, y)

				if foundAdjacentSymbol:
					print(numberString)
					sum += int(numberString)

				x += len(numberString)

			else:

				x += 1

	print("Sum = " + str(sum))


def main_part2():

	f = open("input.txt", "r")

	sum = 0

	fullInput = f.readlines();

	# Strip out new lines.
	for index in range(len(fullInput)):
		fullInput[index] = fullInput[index].strip('\n')

	print(fullInput)

	numRows = len(fullInput)
	numCols = len(fullInput[0])

	coordsDict = {}
	coordsMultiDict = {}

	for y in range(numRows):
		
		x = 0

		while(x < numCols):

			numberString = extractNumber(fullInput, x, y, numCols)

			if (numberString != ""):

				print("Found " + numberString)

				allAdjacentSymbolCoords = []

				for ix in range(0, len(numberString)):

					adjacentSymbolCoords = getAdjacentSymbolsCoords(fullInput, x+ix, y, '*')

					for item in adjacentSymbolCoords:
						allAdjacentSymbolCoords.append(item)

				uniqueCoords = np.unique(allAdjacentSymbolCoords)

				for coordIndex in uniqueCoords:
					if coordIndex in coordsDict:
						coordsDict[coordIndex] = coordsDict[coordIndex] + 1
						coordsMultiDict[coordIndex] = coordsMultiDict[coordIndex] * int(numberString)
					else:
						coordsDict[coordIndex] = 1
						coordsMultiDict[coordIndex] = int(numberString)

				x += len(numberString)

			else:

				x += 1

			#coordsMultiDict

	print(coordsDict)
	print(coordsMultiDict)

	for symbolCoord in coordsDict:

		if coordsDict[symbolCoord] != 2:
			continue

		sum += coordsMultiDict[symbolCoord]

		#symbolX = symbolCoord % numCols
		#symbolY = symbolCoord / numCols





	print("Sum = " + str(sum))


def extractNumber(fullInput, x, y, numCols):

	numberString = ""

	index = 0

	while(True):
		char = fullInput[y][x+index]

		if not (char.isnumeric()):
			break

		numberString += char

		index += 1
		if(x+index >= numCols):
			break

	return numberString



def isSymbol(char):
	validSymbols = "!@#$%^&*()_-+={}[]\\/"

	if char in validSymbols:
		 return True

	return False


def isValidLookup(x, y, numCols, numRows):

	if(x == 0 and y == 0):	# don't lookup yourself !
		return False

	if(x < 0):
		return False
	if(x > numCols-1):
		return False
	if(y < 0):
		return False
	if(y > numRows-1):
		return False

	return True


def isAdjacentToSymbol(fullInput, x, y):

	numRows = len(fullInput)
	numCols = len(fullInput[0])

	foundSymbol = False

	#print("isAdjacentToSymbol called with x=" + str(x) + " y=" + str(y))

	for ix in range(-1,2):
		for iy in range(-1,2):
			if isValidLookup(x+ix, y+iy, numCols, numRows):
				#print("isAdjacentToSymbol testing x=" + str(x+ix) + " y=" + str(y+iy))
				foundSymbol |= isSymbol(fullInput[y+iy][x+ix])

	return foundSymbol


def getAdjacentSymbolsCoords(fullInput, x, y, symbol):

	results = []

	numRows = len(fullInput)
	numCols = len(fullInput[0])

	for ix in range(-1,2):
		for iy in range(-1,2):

			index = x + ix + ((y+iy) * numCols)

			if not isValidLookup(x+ix, y+iy, numCols, numRows):
				continue
			if not (fullInput[y+iy][x+ix] == symbol):
				continue
			if not (isSymbol(fullInput[y+iy][x+ix])):
				continue
			
			results.append(int(index))

	return results




if __name__ == "__main__":
	main_part2()