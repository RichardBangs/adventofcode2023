import os
import threading
import multiprocessing
import time
import typing

# Problem here: https://adventofcode.com/2023/day/5

#TODO - change to 64 bit value !?
ID = int

class IdRangeMapping:
	sourceStart: ID
	destStart: ID
	range: int

	def __str__(self):

		myString = "\t" + str(self.sourceStart) + "->" + str(self.destStart) + " (Range: " + str(self.range) + ")"
		return myString


# Lookup Table for id range mappings
class IdLookupTable:

	name: str

	idRangeMappings: [IdRangeMapping]


	def __init__(self, name):
		self.name = name
		self.idRangeMappings = []


	def addIdRangeMapping(self, sourceStart, destStart, range):

		idRangeMapping = IdRangeMapping()

		idRangeMapping.sourceStart = sourceStart
		idRangeMapping.destStart = destStart
		idRangeMapping.range = range

		self.idRangeMappings.append(idRangeMapping)


	def lookup(self, id: ID) -> ID:

		for idRangeMapping in self.idRangeMappings:

			if (id < idRangeMapping.sourceStart):
				continue

			if(id >= (idRangeMapping.sourceStart + idRangeMapping.range)):
				continue

			#print(f"Found Mapping {id} : {idRangeMapping}")

			return (id - idRangeMapping.sourceStart) + idRangeMapping.destStart

		return id


	def __str__(self):

		myString = self.name + '\n';

		for mapping in self.idRangeMappings:
			myString += str(mapping) + '\n'

		return myString


def getListOfNumbers(line) -> [int]:

	result = []

	myList = line.split(" ")

	for item in myList:

		if item == "":
			continue

		result.append(int(item))

	return result



def main_part1():

	f = open("input_1.txt", "r")


	seeds: [int] = []
	lookupTables: [IdLookupTable] = []

	fullInput = f.readlines();

	# Populate lookup tables.
	for line in fullInput:

		line = line.strip('\n')

		if(line == ""):
			continue

		if(line.startswith("seeds:")):
			seeds = getListOfNumbers(line.split(':')[1])
			continue

		if(':' in line):
			lookupTables.append(IdLookupTable(line))
			continue

		numbers = getListOfNumbers(line)
		assert len(numbers) == 3

		lookupTables[-1].addIdRangeMapping(numbers[1], numbers[0], numbers[2])


	# Output Source Data.
	print("Seeds = " + str(seeds))

	for lookupTable in lookupTables:
		print(lookupTable)


	lowestLocation = -1

	# Process the Seed Values and calculate the Result.
	for seed in seeds:

		myId = seed

		for lookup in lookupTables:

			newId = lookup.lookup(myId)

			print(f"{myId} -> {lookup.name} -> {newId}")

			myId = newId

		print(f"Seed {seed} maps to location {myId}")

		if(lowestLocation == -1) or (myId < lowestLocation):
			lowestLocation = myId


	print("lowestLocation = " + str(lowestLocation))


def doSeedProcessing(lookupTables: [IdLookupTable], startId : ID, myRange : int) -> ID:

	lowestLocation = -1
	myId = 0

	for index in range(0, myRange):

		seed = startId + index
		myId = seed

		for lookup in lookupTables:

			myId = lookup.lookup(myId)

		if(lowestLocation == -1) or (myId < lowestLocation):
			lowestLocation = myId

	return lowestLocation

results = []

def thread_callback(result):

	jobsRemaining = 0
	for result in results:
		if not (result.ready()):
			jobsRemaining += 1

	print(f"Jobs Remaining:{jobsRemaining}")


def main_part2():

	f = open("input_1.txt", "r")


	seeds: [(int,int)] = []
	lookupTables: [IdLookupTable] = []

	fullInput = f.readlines();

	# Populate lookup tables.
	for line in fullInput:

		line = line.strip('\n')

		if(line == ""):
			continue

		if(line.startswith("seeds:")):
			mySeeds = getListOfNumbers(line.split(':')[1])

			for index in range(0, len(mySeeds), 2):
				seeds.append((mySeeds[index], mySeeds[index+1]))

			continue

		if(':' in line):
			lookupTables.append(IdLookupTable(line))
			continue

		numbers = getListOfNumbers(line)
		assert len(numbers) == 3

		lookupTables[-1].addIdRangeMapping(numbers[1], numbers[0], numbers[2])


	# Output Source Data.
	print("Seeds = " + str(seeds))

	for lookupTable in lookupTables:
		print(lookupTable)

	lowestLocation : ID = -1

	splitSeeds : [(ID,int)] = []
	jobSize = 5000000
	
	for mySeed in seeds:
		
		startId = mySeed[0]
		endId = mySeed[0] + mySeed[1]

		while(startId < endId):

			newEndId = startId + jobSize
			if(newEndId > endId):
				newEndId = endId

			splitSeeds.append((startId, newEndId))
			startId = newEndId

	print(f"Split into {len(splitSeeds)} jobs")

	#def doSeedProcessing(lookupTables: [IdLookupTable], startId : ID, myRange : int) -> ID:

	jobData : [(IdLookupTable, ID, int)] = []

	for seed in splitSeeds:
		jobData.append((lookupTables, seed[0], seed[1]-seed[0]))

	with multiprocessing.Pool(processes = 32) as pool:
		for job in jobData:
			results.append(-1)
			results[-1] = pool.apply_async(doSeedProcessing, job, callback=thread_callback)
		
		pool.close()
		pool.join()

	for result in results:

		if(lowestLocation == -1 or result.get() < lowestLocation):
			lowestLocation = result.get()

	print(f"lowestLocation = {lowestLocation}")




if __name__ == "__main__":

	start = time.time()

	main_part2()

	end = time.time()

	print(f"Runtime: {end-start}")