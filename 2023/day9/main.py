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

	sum = 0

	for index in range(0, len(fullInput)):

		line = fullInput[index]

		line = line.strip('\n')

		if(line == ""):
			continue

		finalValue = processInputRow(getListOfNumbers(line))

		print(f"{line} -> {finalValue}")

		sum += finalValue

	print(f"Sum = {sum}")



def processInputRow(input : [int]) -> int:

	newRow : [int] = []

	allZero = True

	for index in range(1,len(input)):
		diff = input[index] - input[index-1]
		newRow.append(diff)

		if(diff != 0):
			allZero = False

	if(allZero):
		return input[-1]

	return input[-1] + processInputRow(newRow)


def getListOfNumbers(line) -> [int]:

	result = []

	myList = line.split(" ")

	for item in myList:

		if item == "":
			continue

		result.append(int(item))

	return result



def main_part2():

	hands : [(int, int)] = []

	f = open("input_1.txt", "r")

	# Populate inputs.
	fullInput = f.readlines();

	sum = 0

	for index in range(0, len(fullInput)):

		line = fullInput[index]

		line = line.strip('\n')

		if(line == ""):
			continue

		numList = getListOfNumbers(line)
		numList.reverse()

		finalValue = processInputRow(numList)

		print(f"{finalValue} -> {line}")

		sum += finalValue

	print(f"Sum = {sum}")




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
	print("Day 9 - Timings")

	for index in range(0, len(name)):
		print (f"{name[index]}{((end[index]-start[index])*1000):,.2f}ms")
