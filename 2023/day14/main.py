import os
import sys
from copy import deepcopy

class NodeType():
	ROCK = 'O'
	STOP = '#'
	EMPTY = '.'


def rollNorth(area : [[chr]]) -> [[chr]]:

	newArea = deepcopy(area)

	numRows = len(newArea)
	numCols = len(newArea[0])

	for x in range(numCols):
		for startY in range(numRows):

			if(newArea[startY][x] != NodeType.ROCK):
				continue

			#	We have a ROCK, roll it up until we get to a # or array bounds.
			for endY in range(startY-1, -1, -1):

				if(newArea[endY][x] != NodeType.EMPTY):
					break

				newArea[endY][x] = NodeType.ROCK
				newArea[endY+1][x] = NodeType.EMPTY

	return newArea

def rollCycle(area : [[chr]]) -> [[chr]]:

	newArea = deepcopy(area)

	numRows = len(newArea)
	numCols = len(newArea[0])

	# NORTH
	for x in range(numCols):
		for startY in range(numRows):

			if(newArea[startY][x] != NodeType.ROCK):
				continue

			#	We have a ROCK, roll it up until we get to a # or array bounds.
			for endY in range(startY-1, -1, -1):

				if(newArea[endY][x] != NodeType.EMPTY):
					break

				newArea[endY][x] = NodeType.ROCK
				newArea[endY+1][x] = NodeType.EMPTY

	# WEST
	for y in range(numRows):
		for startX in range(numCols):
		
			if(newArea[y][startX] != NodeType.ROCK):
				continue

			#	We have a ROCK, roll it up until we get to a # or array bounds.
			for endX in range(startX-1, -1, -1):

				if(newArea[y][endX] != NodeType.EMPTY):
					break

				newArea[y][endX] = NodeType.ROCK
				newArea[y][endX+1] = NodeType.EMPTY

	# SOUTH
	for x in range(numCols):
		for startY in range(numRows-1, -1, -1):

			if(newArea[startY][x] != NodeType.ROCK):
				continue

			#	We have a ROCK, roll it up until we get to a # or array bounds.
			for endY in range(startY+1, numRows):

				if(newArea[endY][x] != NodeType.EMPTY):
					break

				newArea[endY][x] = NodeType.ROCK
				newArea[endY-1][x] = NodeType.EMPTY

	# EAST
	for y in range(numRows):
		for startX in range(numCols-1, -1, -1):
		
			if(newArea[y][startX] != NodeType.ROCK):
				continue

			#	We have a ROCK, roll it up until we get to a # or array bounds.
			for endX in range(startX+1, numCols):

				if(newArea[y][endX] != NodeType.EMPTY):
					break

				newArea[y][endX] = NodeType.ROCK
				newArea[y][endX-1] = NodeType.EMPTY

	return newArea


def countNorth(area : [[chr]]) -> int:

	numRows = len(area)
	numCols = len(area[0])

	sum = 0

	for x in range(numCols):
		for y in range(numRows):

			if(area[y][x] != NodeType.ROCK):
				continue

			sum += numRows - y



	return sum


def printArea(area : [[chr]]):
	for q in area:
		print(q)


def main_part1(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	numRows = len(fullInput)
	numCols = len(fullInput[0])
	
	area : [[chr]] = []


	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

		myRow : [chr] = []

		for col in range(0, len(line)):
			myRow.append(fullInput[row][col])

		area.append(myRow)
	

	areaRollNorth = rollNorth(area)

	print("Area:")
	printArea(area)

	print("Area RolledNorth:")
	printArea(areaRollNorth)

	northLoad = countNorth(areaRollNorth)

	print(northLoad)

	return northLoad



def main_part2(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	numRows = len(fullInput)
	numCols = len(fullInput[0])
	
	area : [[chr]] = []


	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

		myRow : [chr] = []

		for col in range(0, len(line)):
			myRow.append(fullInput[row][col])

		area.append(myRow)
	
	allLoads : [int] = []

	for q in range(0, 1000):
		area = rollCycle(area)
		northLoad = countNorth(area)

		allLoads.append(northLoad)
	

	endVal = allLoads[-1]
	endIdx = len(allLoads)-1
	startIdx = 0
	for q in range(endIdx-1, 0, -1):
		if(allLoads[q] != endVal):
			continue

		startIdx = q
		break

	offset = (1000000000 - endIdx) % (endIdx - startIdx)

	val = allLoads[startIdx + offset - 1]

	print(val)

	return val




	#print("Area:")
	#printArea(area)

	#print("Area RollCycle:")
	#printArea(areaRollCycle)

	#return northLoad



argPart : int = int(sys.argv[1])
argInputFile : str = sys.argv[2]

retVal = 0

if(argPart == 1):
	retVal = main_part1(argInputFile)
else:
	retVal = main_part2(argInputFile)

sys.exit(retVal)