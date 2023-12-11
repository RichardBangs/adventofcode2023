import os
import time

class Node:

	Location : str = ""
	Left = None
	Right = None

	def __init__(self, Location : str):
		self.Location = Location


def main_part1():

	hands : [(int, int)] = []

	f = open("input_1.txt", "r")

	# Populate inputs.
	fullInput = f.readlines();

	inputInstruct : str = ""
	inputData : [(str, str, str)] = []

	for index in range(0, len(fullInput)):

		line = fullInput[index]

		line = line.strip('\n')

		if(index == 0):
			inputInstruct = line
			continue

		if(line == ""):
			continue

		line = line.replace(' ', '')
		line = line.replace('(', '')
		line = line.replace(')', '')

		location = line.split('=')[0]
		
		left = line.split('=')[1].split(',')[0]
		right = line.split('=')[1].split(',')[1]

		inputData.append((location, left, right))

	allNodes : Node = constructTree(inputInstruct, inputData)

	rootNode : Node = None

	for key,value in allNodes.items():
		if(value.Location == "AAA"):
			rootNode = value
			break

	numSteps = walkTree(rootNode, inputInstruct)

	print(numSteps)



def findNode(node : Node, location : str) -> Node:

	if(node == str):
		return node

	leftTest = findNode(node.Left, str)
	if(leftTest != None):
		return leftTest

	rightTest = findNode(node.Right, str)
	if(rightTest != None):
		return rightTest

	return None



def constructTree(inputInstruct : str, inputData : [(str, str, str)]) -> {str, Node}:

	nodesAdded : {str, Node} = {}

	for data in inputData:
		newNode = Node(data[0])
		nodesAdded[data[0]] = newNode

	for index in range(0, len(inputData)):
		location = inputData[index][0]
		left = inputData[index][1]
		right = inputData[index][2]

		nodesAdded[location].Left = nodesAdded[left]
		nodesAdded[location].Right = nodesAdded[right]

	return nodesAdded


def walkTree(rootNode : Node, inputInstruct : str) -> int:
	
	numSteps = 0
	currentNode : Node = rootNode

	while(True):

		if(currentNode.Location == "ZZZ"):
			break

		if(inputInstruct[numSteps % len(inputInstruct)] == 'L'):
			currentNode = currentNode.Left
		else:
			currentNode = currentNode.Right

		numSteps += 1


	return numSteps

def stepTree(rootNode : Node, inputInstruct : chr) -> Node:
	
	currentNode : Node = rootNode

	if(inputInstruct == 'L'):
		currentNode = currentNode.Left
	else:
		currentNode = currentNode.Right

	return currentNode


def main_part2():

	hands : [(int, int)] = []

	f = open("input_1.txt", "r")

	# Populate inputs.
	fullInput = f.readlines();

	inputInstruct : str = ""
	inputData : [(str, str, str)] = []

	for index in range(0, len(fullInput)):

		line = fullInput[index]

		line = line.strip('\n')

		if(index == 0):
			inputInstruct = line
			continue

		if(line == ""):
			continue

		line = line.replace(' ', '')
		line = line.replace('(', '')
		line = line.replace(')', '')

		location = line.split('=')[0]
		
		left = line.split('=')[1].split(',')[0]
		right = line.split('=')[1].split(',')[1]

		inputData.append((location, left, right))

	nodeDict = constructTree(inputInstruct, inputData)

	nodeList : [Node] = []

	for location,potentialStartNode in nodeDict.items():
		if location[-1] == 'A':
			nodeList.append(potentialStartNode)

	bruteForce = False

	if(bruteForce):

		numSteps = 0

		while(True):

			allComplete = True
			for node in nodeList:
				if(node.Location[-1] != 'Z'):
					allComplete = False
					break

			if(allComplete):
				break

			for index in range(0, len(nodeList)):
				nodeList[index] = stepTree(nodeList[index], inputInstruct[numSteps % len(inputInstruct)])

			numSteps += 1

			if(numSteps%100000000 == 0):
				print(numSteps)
	else:

		nodeListResults : [] = []

		for index in range(0, len(nodeList)):

			numSteps = 0

			while(nodeList[index].Location[-1] != 'Z'):
				nodeList[index] = stepTree(nodeList[index], inputInstruct[numSteps % len(inputInstruct)])

				numSteps += 1

			nodeListResults.append(numSteps)

		sum : int = 1
		#for result in nodeListResults:
		#	sum *= result

		print(nodeListResults)

		testValue = nodeListResults[0]

		while(True):
			
			passed = True
			for result in nodeListResults:
				if testValue % result != 0:
					passed = False
					break

			if(passed):
				print(f"FOUND {testValue}")
				break

			testValue += nodeListResults[0]
			if(testValue % 1000000000 == 0):
				print(testValue)


if __name__ == "__main__":

	name = []
	start = []
	end = []

	name.append("Part 1:  ")
	start.append(time.time())
	print("Executing: Part 1")
	main_part1()
	end.append(time.time())

	name.append("Part 2:  ")
	start.append(time.time())
	print("Executing: Part 2")
	main_part2()
	end.append(time.time())

	print("")
	print("Day 8 - Timings")

	for index in range(0, len(name)):
		print (f"{name[index]}{((end[index]-start[index])*1000):,.2f}ms")
