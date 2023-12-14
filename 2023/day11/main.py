import os
import sys


class Node:

	Empty : int = 0

	planetId : int = 0

	x : int = 0
	y : int = 0

	def __init__(self, x : int, y : int) -> bool:
		self.planetId = self.Empty
		self.x = x
		self.y = y

	def isEmpty(self) -> bool:
		return self.planetId == self.Empty


class Universe:

	data : [Node] = []

	numPlanets : int = 0

	maxX : int = 0
	maxY : int = 0

	def __init__(self, maxX, maxY):
		
		self.maxX = maxX
		self.maxY = maxY
		self.data = []

		for y in range(0, maxY):
			for x in range(0, maxX):
				self.data.append(Node(x, y))

	def insert(self, myChar : chr, x : int, y : int):

		if(myChar == '#'):
			self.numPlanets += 1
			self.at(x, y).planetId = self.numPlanets
		else:
			self.at(x, y).planetId = 0

	def index(self, x : int, y : int) -> int:
		return (y * self.maxX) + x

	def at(self, x : int, y : int) -> Node:
		return self.data[self.index(x, y)]

	def getPlanetById(self, planetId : int) -> Node:
		for node in self.data:
			if(node.planetId == planetId):
				return node;
		return None

	def addPlanet(self, node : Node):
		self.numPlanets += 1
		self.data[self.index(node.x, node.y)] = node

	def isRowEmpty(self, y : int) -> bool:
		for x in range(0, self.maxX):
			if not self.at(x, y).isEmpty():
				return False
		return True

	def isColEmpty(self, x : int) -> bool:
		for y in range(0, self.maxY):
			if not self.at(x, y).isEmpty():
				return False
		return True


def outputUniverse(universe : Universe):

	outputString : str = ""

	for y in range(0, universe.maxY):
		for x in range(0, universe.maxX):

			myNode : Node = universe.at(x, y)

			if(myNode.planetId == Node.Empty):
				outputString += '.'
			else:
				outputString += str(myNode.planetId)

		outputString += '\n'


	print(outputString)




def populateUniverse(fullInput : str) -> Universe:

	maxX = len(fullInput[0])-1
	maxY = len(fullInput)

	universe : Universe = Universe(maxX, maxY)


	# Populate from input.
	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

		for col in range(0, len(line)):
			universe.insert(line[col], col, row)
	
	return universe


def expandUniverse(uIn : Universe) -> Universe:

	emptyX : [int] = []
	emptyY : [int] = []

	for y in range(0, uIn.maxY):
		isRowEmpty = True
		for x in range(0, uIn.maxX):
			if not uIn.at(x, y).isEmpty():
				isRowEmpty = False
				break

		if(isRowEmpty):
			emptyY.append(y)

	for x in range(0, uIn.maxX):
		isColEmpty = True
		for y in range(0, uIn.maxY):
			if not uIn.at(x, y).isEmpty():
				isColEmpty = False
				break

		if(isColEmpty):
			emptyX.append(x)

	uOut : Universe = Universe(uIn.maxX + len(emptyX), uIn.maxY + len(emptyY))

	for planetId in range(1, uIn.numPlanets+1):

		oldNode = uIn.getPlanetById(planetId)
		

		offsetX = 0
		for testX in emptyX:
			if(testX < oldNode.x):
				offsetX += 1
			else:
				break

		offsetY = 0
		for testY in emptyY:
			if(testY < oldNode.y):
				offsetY += 1
			else:
				break

		newNode = Node(oldNode.x + offsetX, oldNode.y + offsetY)
		newNode.planetId = oldNode.planetId
		uOut.addPlanet(newNode)

	return uOut


def planetPathfind(universe : Universe, startPlanetId : int, endPlanetId : int) -> int:

	numSteps : int = 0

	currentNode : Node = universe.getPlanetById(startPlanetId)
	endNode : Node = universe.getPlanetById(endPlanetId)

	while(currentNode != endNode):

		dx = endNode.x - currentNode.x
		dy = endNode.y - currentNode.y

		if(abs(dx) > abs(dy)):
			if(dx > 0):
				currentNode = universe.at(currentNode.x + 1, currentNode.y)
			else:
				currentNode = universe.at(currentNode.x - 1, currentNode.y)
		else:
			if(dy > 0):
				currentNode = universe.at(currentNode.x, currentNode.y + 1)
			else:
				currentNode = universe.at(currentNode.x, currentNode.y - 1)

		numSteps += 1

	return numSteps


def planetPathfind2(universe : Universe, startPlanetId : int, endPlanetId : int) -> int:

	numSteps : int = 0

	currentNode : Node = universe.getPlanetById(startPlanetId)
	endNode : Node = universe.getPlanetById(endPlanetId)

	emptyColRowCost : int = 1000000

	while(currentNode != endNode):

		dx = endNode.x - currentNode.x
		dy = endNode.y - currentNode.y

		if(abs(dx) > abs(dy)):
			if(dx > 0):
				currentNode = universe.at(currentNode.x + 1, currentNode.y)
			else:
				currentNode = universe.at(currentNode.x - 1, currentNode.y)

			if(universe.isColEmpty(currentNode.x)):
				numSteps += emptyColRowCost
			else:
				numSteps += 1

		else:
			if(dy > 0):
				currentNode = universe.at(currentNode.x, currentNode.y + 1)
			else:
				currentNode = universe.at(currentNode.x, currentNode.y - 1)

			if(universe.isRowEmpty(currentNode.y)):
				numSteps += emptyColRowCost
			else:
				numSteps += 1

	return numSteps


def getAllPairs(numPlanets : int) -> [(int, int)]:

	result : [(int, int)] = []

	for p in range(1, numPlanets):
		for q in range(p+1, numPlanets):
			result.append((p, q))

	return result


def main_part1(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines()

	universe = populateUniverse(fullInput)

	print("Original:")
	outputUniverse(universe)

	universe2 = expandUniverse(universe)

	print("Expanded:")
	outputUniverse(universe2)
	
	sum = 0
	planetPairs : [(int, int)] = getAllPairs(universe2.numPlanets+1)
	for planetPair in planetPairs:
		sum += planetPathfind(universe2, planetPair[0], planetPair[1])

	print(sum)

	return sum



def main_part2(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines()

	universe = populateUniverse(fullInput)

	print("Original:")
	outputUniverse(universe)
	
	sum = 0
	planetPairs : [(int, int)] = getAllPairs(universe.numPlanets+1)
	for planetPair in planetPairs:
		sum += planetPathfind2(universe, planetPair[0], planetPair[1])

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