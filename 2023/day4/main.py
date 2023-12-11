import os
import sys 


def main_part1():

	f = open("input_1.txt", "r")

	sum = 0

	fullInput = f.readlines();

	for line in fullInput:

		line = line.strip('\n')

		cardNumberString = line.split(':')[0]
		winningNumbers = line.split(':')[1].split('|')[0]
		cardNumbers = line.split(':')[1].split('|')[1]

		print(cardNumberString)
		print("winningNumbers = " + str(getListOfNumbers(winningNumbers)))
		print("cardNumbers = " + str(getListOfNumbers(cardNumbers)))

		result = getNumItemsThatExistInBothLists(getListOfNumbers(cardNumbers), getListOfNumbers(winningNumbers))

		if result == 0:
			powerResult	= 0
		else:
			powerResult = pow(2, result-1)

		print("Points = " + str(powerResult) + "    matches=" + str(result))

		sum += powerResult


	print("Sum = " + str(sum))


def main_part2():

	f = open("input_2.txt", "r")

	sum = 0

	fullInput = f.readlines();

	#	index of these arrays corrisponds to the index of a single, original scratchcard
	scratchcardsOriginal = []	# read only...
	scratchcardsWinCount = []	# how many times a specific original scratchcard has won

	jobQueue = []	# list of original scratch card ids we need to process


	for index in range(0, len(fullInput)):

		line = fullInput[index]

		line = line.strip('\n')

		winningNumbers = line.split(':')[1].split('|')[0]
		cardNumbers = line.split(':')[1].split('|')[1]

		scratchcardsOriginal.append((getListOfNumbers(winningNumbers), getListOfNumbers(cardNumbers)))
		scratchcardsWinCount.append(0)

		jobQueue.append(index)

	
	while(len(jobQueue) > 0):

		scratchcardId = jobQueue.pop(len(jobQueue)-1)

		winningNumbers = scratchcardsOriginal[scratchcardId][0]
		cardNumbers = scratchcardsOriginal[scratchcardId][1]

		#print("card = " + str(scratchcardId+1))
		#print("winningNumbers = " + str(winningNumbers))
		#print("cardNumbers = " + str(cardNumbers))

		result = getNumItemsThatExistInBothLists(cardNumbers, winningNumbers)

		#print(result)

		scratchcardsWinCount[scratchcardId] += 1
		sum += 1

		for index in range(0, result):
			jobQueue.append(scratchcardId+index+1)

		if sum % 1000 == 0:
			print("Remaining: " + str(len(jobQueue)))

	print("Sum = " + str(sum))


def getListOfNumbers(line):

	result = []

	myList = line.split(" ")

	for item in myList:

		if item == "":
			continue

		result.append(int(item))

	return result


def getNumItemsThatExistInBothLists(listA, listB):

	result = 0

	for itemA in listA:

		found = False

		for itemB in listB:
			if itemA == itemB:
				found = True
				break

		if found:
			result += 1

	return result


if __name__ == "__main__":
	main_part2()