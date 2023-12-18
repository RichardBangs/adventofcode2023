import os
import sys
import threading
import multiprocessing
from multiprocessing import freeze_support


class NodeType():
	MAYBE = '?'
	SPRING = '#'
	EMPTY = '.'


def isValid(layout : [NodeType], criteria : [int]):

	layoutLen = len(layout)
	layoutIndex = 0

	#print(f"layout={layout} crit={criteria}")

	for crit in criteria:

		if layoutIndex >= layoutLen:
			return False

		#	Find next spring.
		while(layoutIndex < layoutLen):

			myChar = layout[layoutIndex]
			
			if(myChar == NodeType.EMPTY):
				layoutIndex += 1
				continue

			if(myChar == NodeType.SPRING):
				break

			assert(False)
			return False

		#	Find next end
		layoutIndex += 1
		springCounter = 1
		while(layoutIndex < layoutLen):
			
			myChar = layout[layoutIndex]

			if(myChar == NodeType.SPRING):
				layoutIndex += 1
				springCounter += 1
				continue

			if(myChar == NodeType.EMPTY):
				break

			assert(False)
			return False

		if(springCounter != int(crit)):
			return False

	return True


def loadLayout(line : str) -> ([chr], [int]):

	result : ([chr], [int]) = ([], [])

	result = (line.split(' ')[0], line.split(' ')[1].split(','))

	return result


def loadLayout2(line : str) -> ([chr], [int]):

	result : ([chr], [int]) = ([], [])

	springs = line.split(' ')[0]
	groups = line.split(' ')[1].split(',')

	springs2 = ""
	groups2 = []
	for index in range(0, 5):
		springs2 += springs
		if(index < 4):
			 springs2 += "?"

		for num in groups:
			groups2.append(num)

	result = (springs2, groups2)

	return result



def getPermutations(layout : [NodeType], criteria : [int]) -> int:

	critSum = 0
	for x in criteria:
		critSum += int(x)


	missing = critSum - layout.count(NodeType.SPRING)
	maxSkip = layout.count(NodeType.MAYBE)-missing
	layoutLen = len(layout)

	found : [str] = []

	counters : [int] = []
	for q in range(0, missing):
		counters.append(0)

	result = 0

	if(missing == 0):
		temp = layout.replace("?", ".");
		if(isValid(temp, criteria)):
			result += 1

	tested = 0

	#print(f"layo={layout} critSum={critSum} missing={missing} maxSkip={maxSkip}")

	while(True):
		temp = "" + layout

		layoutIndex = 0

		#print("")
		#print(temp)
		#print(f"missing={missing}")
		#print(f"counters={counters}")

		placed = False

		for q in range(0, missing):

			placed = False
			counter = 0
			
			while(layoutIndex < layoutLen):
				
				if(placed):
					break
#				print(f"\t\tlayoutIndex={layoutIndex}")

				if(temp[layoutIndex] != NodeType.MAYBE):
					layoutIndex += 1
					continue

				if(counter < counters[q]):
					layoutIndex += 1
					counter += 1
					continue

				temp = temp[:layoutIndex] + NodeType.SPRING + temp[layoutIndex + 1:]
				placed = True

				#print(f"layoutIndex={layoutIndex} counter={counter} temp={temp}")

			tested += 1

			if(q < missing-1):
				if(temp[layoutIndex+1] == NodeType.MAYBE or temp[layoutIndex+1] == NodeType.SPRING):
					if(counters[q+1] == 0):
						placed = False
						break


		#print(f"temp={temp} placed={placed} counters={counters}")

		if(placed):

			temp = temp.replace("?", ".")

			if not (temp in found):
				if(isValid(temp, criteria)):
					#print(f"Valid {temp} {criteria}")
					result += 1
					found.append(temp)

		counterIndex = 0
		
		while(True):
			while(counterIndex < missing):
				counters[counterIndex] += 1
				
				numSkip = 0
				for q in range(0, counterIndex):
					numSkip = counters[q]

				if(numSkip > maxSkip or (counters[counterIndex]) > maxSkip):

					#print(f"counterIndex={counterIndex} missing={missing}")

					if(counterIndex >= missing):
						counterIndex += 1
						break

					#if(counterIndex+1 >= int(missing)):
					#	break

					counters[counterIndex] = 0
					#counters[counterIndex+1] = counters[counterIndex+1]+1

					counterIndex += 1

					if(counterIndex >= missing):
						break

				else:
					break

			if(counterIndex >= missing):
				break

			numSkip = 0
			for q in counters:
				numSkip += q

			#print(f"{numSkip} {maxSkip}")
			if(numSkip <= maxSkip):
				break



		if(counterIndex >= missing):
			print(f"tested {tested}")
			return result

	return 0


results = []

def thread_callback(result):

	jobsRemaining = 0
	for result in results:
		if(result == None):
			continue
		if not (result.ready()):
			jobsRemaining += 1

	print(f"Jobs Remaining:{jobsRemaining}")


def main_part1(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	multiThread = True

	if not multiThread:
		# Populate allNodes from inputFile
		for row in range(0, len(fullInput)):

			line = fullInput[row].strip('\n')

			if(line == ""):
				continue

			#if(row != 1):
			#	continue

			layoutInfo = loadLayout(line)

			numPermutations = getPermutations(layoutInfo[0], layoutInfo[1])

			#print(f"{layoutInfo[0]} {layoutInfo[1]} -> {numPermutations}")

			sum += numPermutations

	else:

		jobData : [(str, [int])] = []

		for row in range(0, len(fullInput)):

			line = fullInput[row].strip('\n')

			if(line == ""):
				continue

			jobData.append(loadLayout(line))
			#numPermutations = getPermutations(layoutInfo[0], layoutInfo[1])

			#print(f"{layoutInfo[0]} {layoutInfo[1]} -> {numPermutations}")

			#sum += numPermutations

			#break
		
		with multiprocessing.Pool(processes = 32) as pool:
			for job in jobData:
				results.append(pool.apply_async(getPermutations, job, callback=thread_callback))
			
			pool.close()
			pool.join()

		for result in results:
			sum += result.get()

	print(sum)

	return sum

def main_part2(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	multiThread = False

	if not multiThread:
		# Populate allNodes from inputFile
		for row in range(0, len(fullInput)):

			line = fullInput[row].strip('\n')

			if(line == ""):
				continue

			layoutInfo = loadLayout2(line)
			print(layoutInfo)

			numPermutations = getPermutations(layoutInfo[0], layoutInfo[1])

			#print(f"{layoutInfo[0]} {layoutInfo[1]} -> {numPermutations}")

			sum += numPermutations

	else:

		jobData : [(str, [int])] = []

		for row in range(0, len(fullInput)):

			line = fullInput[row].strip('\n')

			if(line == ""):
				continue

			jobData.append(loadLayout2(line))
		
		with multiprocessing.Pool(processes = 32) as pool:
			for job in jobData:
				results.append(pool.apply_async(getPermutations, job, callback=thread_callback))
			
			pool.close()
			pool.join()

		for result in results:
			sum += result.get()

	print(sum)

	return sum


resultCache = {}


def recursePermutations(left : str, crit : [int], other : str) -> int:

	key = "" + left
	for q in crit:
		key += str(q) + ','

	if(key in resultCache):
		return resultCache[key]

	sum = 0

	index = 0

	#print(f"recurse={other}{left} process={left} crit={crit}")

	myChar = ''

	while(True):

		if(index >= len(left)):
			break

		myChar : chr = left[index]

		if(myChar == NodeType.EMPTY):
			index += 1
		else:
			break

	if(index >= len(left)):
		if(len(crit) == 0):
			#print(f"FOUND A = {other}{left}")
			return 1
		return 0

	if(len(crit) == 0):
		if(NodeType.SPRING in left):
			return 0
		else:
			#print(f"FOUND B = {other}{left}")
			return 1

	if(myChar == NodeType.MAYBE):
		sum += recursePermutations(NodeType.SPRING + left[index + 1:], crit, other + left[:index])
		sum += recursePermutations(NodeType.EMPTY + left[index + 1:], crit, other + left[:index])
	elif(myChar == NodeType.SPRING):
		#consume crit and test string as we go

		crit = crit.copy()

		numSkip = int(crit.pop(0))

		for skipIndex in range(0, numSkip):
			if(skipIndex+index >= len(left)):
				return 0
			if(left[skipIndex+index] == NodeType.EMPTY):
				return 0

		newIndex = index+numSkip

		if(newIndex+1 <= len(left)):
			if(left[newIndex] == NodeType.SPRING):
				return 0

		sum += recursePermutations(left[newIndex+1:], crit, other + left[:newIndex+1])

	resultCache[key] = sum

	return sum


def main_part3(inputFile : str) -> int:

	f = open(inputFile, "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	# Populate allNodes from inputFile
	for row in range(0, len(fullInput)):

		line = fullInput[row].strip('\n')

		if(line == ""):
			continue

		layoutInfo = loadLayout2(line)
		print(layoutInfo)

		resultCache.clear()

		numPermutations = recursePermutations(layoutInfo[0], layoutInfo[1], "")
		#print(f"numPermutations={numPermutations}")

		sum += numPermutations

	print(sum)

	return sum







if __name__ == '__main__':
	freeze_support()
	argPart : int = int(sys.argv[1])
	argInputFile : str = sys.argv[2]
	if(argPart == 1):
		main_part1(argInputFile)
	elif(argPart == 2):
		main_part2(argInputFile)
	else:
		main_part3(argInputFile)
