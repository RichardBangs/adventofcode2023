import os
import sys
from enum import Enum


class style():    
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

class Node:

	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

	# North, East, South, West...
	GoemConnections : [] = [None, None, None, None]
	PipeConnections : [] = [None, None, None, None]

	Type : chr = '.'

	Result : int = -1

	X : int = 0
	Y : int = 0

	def __init__(self, char):
		self.Type = char

	def linkTo(self, dir : int):

		self.PipeConnections[dir] = self.GoemConnections[dir]

	def hasLink(self, testNode) -> bool:

		for node in self.PipeConnections:
			if node == testNode:
				return True

		return False

	def __str__(self):
		myString = "\t" + str(self.Type)
		return myString



def getNodeGraph(fullInput : str) -> [[Node]]:

	maxX = len(fullInput[0])
	maxY = len(fullInput)

	allNodes = [[0]*maxX]*maxY

	# Populate allNodes from inputFile
	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

		lineNodes : [Node] = []

		for char in line:
			lineNodes.append(Node(char))

		allNodes[row] = lineNodes

	maxY = len(allNodes)
	maxX = len(allNodes[maxY-1])

	for y in range(0, maxY):
		for x in range(0, maxX):
			allNodes[y][x].X = x
			allNodes[y][x].Y = y

			allNodes[y][x].GoemConnections = [None, None, None, None]
			allNodes[y][x].PipeConnections = [None, None, None, None]
	
	# Link up all Geom Connections
	for y in range(0, maxY):
		for x in range(0, maxX):

			if(y > 0):
				allNodes[y][x].GoemConnections[0] = allNodes[y-1][x]

			if(x < maxX-1):
				allNodes[y][x].GoemConnections[1] = allNodes[y][x+1]

			if(y < maxY-1):
				allNodes[y][x].GoemConnections[2] = allNodes[y+1][x]

			if(x > 0):
				allNodes[y][x].GoemConnections[3] = allNodes[y][x-1]

	# Link up all Pipe Connections
	for y in range(0, maxY):
		for x in range(0, maxX):

			match allNodes[y][x].Type:
				case '|':
					allNodes[y][x].linkTo(Node.NORTH)
					allNodes[y][x].linkTo(Node.SOUTH)
				case '-':
					allNodes[y][x].linkTo(Node.EAST)
					allNodes[y][x].linkTo(Node.WEST)
				case 'L':
					allNodes[y][x].linkTo(Node.NORTH)
					allNodes[y][x].linkTo(Node.EAST)
				case 'J':
					allNodes[y][x].linkTo(Node.NORTH)
					allNodes[y][x].linkTo(Node.WEST)
				case '7':
					allNodes[y][x].linkTo(Node.SOUTH)
					allNodes[y][x].linkTo(Node.WEST)
				case 'F':
					allNodes[y][x].linkTo(Node.SOUTH)
					allNodes[y][x].linkTo(Node.EAST)
				case 'S':
					allNodes[y][x].linkTo(Node.NORTH)
					allNodes[y][x].linkTo(Node.EAST)
					allNodes[y][x].linkTo(Node.SOUTH)
					allNodes[y][x].linkTo(Node.WEST)

	return allNodes


def debugOutput(allNodes : [[Node]], loopList : [Node], insideList : [Node]):

	maxY = len(allNodes)
	maxX = len(allNodes[maxY-1])

	rangeMinX = 0
	rangeMaxX = 0
	rangeMinY = 0
	rangeMaxY = 0

	for y in range(0, maxY):
		for x in range(0, maxX):
			myNode : Node = allNodes[y][x]

			if(myNode.Type == '.'):
				continue

			if(x < rangeMinX):
				rangeMinX = x
			if(x > rangeMaxX):
				rangeMaxX = x

			if(y < rangeMinY):
				rangeMinY = y
			if(y > rangeMaxY):
				rangeMaxY = y

	rangeMinX -= 2
	rangeMaxX += 2
	rangeMinY -= 2
	rangeMaxY += 2

	if(rangeMinX < 0):
		rangeMinX = 0
	if(rangeMaxX >= maxX):
		rangeMaxX = maxX
	if(rangeMinY < 0):
		rangeMinY = 0
	if(rangeMaxY >= maxY):
		rangeMaxY = maxY

	sum = 0

	fullOutput = True
	if(fullOutput):

		outType = ""

		for y in range(rangeMinY, rangeMaxY):

			for x in range(rangeMinX, rangeMaxX):

				if(allNodes[y][x] in loopList):
					outType += f"{style.RED}{allNodes[y][x].Type}{style.RESET}"
				elif(insideList != None and allNodes[y][x] in insideList):
					outType += f"{style.BLUE}{allNodes[y][x].Type}{style.RESET}"
					sum += 1
				else:
					outType += allNodes[y][x].Type

			outType += '\n'

		print(outType)

	print(f"new SUM -> {sum}")

def getLoopList(allNodes : [[Node]]) -> [Node]:

	maxY = len(allNodes)
	maxX = len(allNodes[maxY-1])

	startingNode = getStartingNode(allNodes)

	for initialDir in range(0,4):

		currentNode = startingNode.PipeConnections[initialDir]

		if currentNode == None:
			continue

		myList = []

		numSteps = 1
		myList.append(startingNode)

		print(f"currentNode={currentNode}" )

		if not (currentNode.hasLink(startingNode)):
			continue



		if not (startingNode.hasLink(currentNode)):
			continue

		myList.append(currentNode)

		while(currentNode != None):

			finished = True

			for potentialNode in currentNode.PipeConnections:

				if(potentialNode == None):
					#print(f"\tConnection = None")
					continue

				if(len(myList) > 2 and potentialNode == startingNode):
					myList.append(potentialNode)
					finished = True

				if(potentialNode in myList):
					continue

				if not (potentialNode.hasLink(currentNode)):
					continue

				currentNode = potentialNode

				myList.append(currentNode)
				finished = False

				break

			if(finished):
				break

			numSteps += 1

		if(myList[-1] == startingNode):
			for item in myList:
				print(f"{item.X},{item.Y} {item.Type}")
			return myList


def getStartingNode(allNodes : [[Node]]) -> Node:

	maxY = len(allNodes)
	maxX = len(allNodes[maxY-1])

	for y in range(0, maxY):
		for x in range(0, maxX):
			if(allNodes[y][x].Type == 'S'):
				return allNodes[y][x]


def main_part1(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	allNodes : [[Node]] = getNodeGraph(fullInput)

	loopList : [Node] = getLoopList(allNodes)

	debugOutput(allNodes, loopList, None)

	maxDistance = int((len(loopList)-1)/2)

	print(f"maxDistance = {maxDistance}")

	return maxDistance






def main_part2(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	allNodes : [[Node]] = getNodeGraph(fullInput)

	loopList : [Node] = getLoopList(allNodes)

	insideList : [Node] = []

	#debugOutput(allNodes, loopList)

	maxY = len(allNodes)
	maxX = len(allNodes[maxY-1])

	for index in range(1, len(loopList)):

		myMin = -1
		myMax = 1


		for splatter in range(myMin, myMax):

			node = loopList[index]
			prev = loopList[index-1]

			deltaX = node.X - prev.X
			deltaY = node.Y - prev.Y

			# 0,1 -> 1,0 -> 0,-1 -> -1,0
			insideX = node.X + deltaY
			insideY = node.Y + -deltaX

			insideX += splatter * deltaX
			insideY += splatter * deltaY

			if insideX < 0:
				continue
			if insideX >= maxX:
				continue
			if insideY < 0:
				continue
			if insideY >= maxY:
				continue

			insideNode = allNodes[insideY][insideX]

			if not (insideNode in insideList) and not (insideNode in loopList):
				insideList.append(allNodes[insideY][insideX])

	print(len(insideList))


	while(True):

		listSize = len(insideList)

		print(f"size = {listSize}")

		for node in insideList:
			for direction in range(0, 4):

				x = node.X
				y = node.Y

				match direction:
					case 0:
						x += 0
						y += 1
					case 1:
						x += 1
						y += 0
					case 2:
						x += 0
						y += -1
					case 3:
						x += -1
						y += 0

				if(x < 0):
					continue
				if(x >= maxX):
					continue
				if(y < 0):
					continue
				if(y >= maxY):
					continue

				newNode = allNodes[y][x]

				if not (newNode in insideList) and not (newNode in loopList):
					insideList.append(newNode)

		if(len(insideList) == listSize):
			break


	debugOutput(allNodes, loopList, insideList)
	


	return 0




argPart : int = int(sys.argv[1])
argInputFile : str = sys.argv[2]

retVal = 0

if(argPart == 1):
	retVal = main_part1(argInputFile)
else:
	retVal = main_part2(argInputFile)

sys.exit(retVal)