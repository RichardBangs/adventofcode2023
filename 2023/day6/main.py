import os


def main_part1():

	f = open("input_1.txt", "r")

	inputDatas : [(int, int)] = []

	# Populate inputs.
	fullInput = f.readlines();

	times = getListOfNumbers(fullInput[0].split(':')[1])
	distances = getListOfNumbers(fullInput[1].split(':')[1])

	inputDatas = list(zip(times, distances))


	# Calculate Results
	results : [int] = []

	print(inputDatas)

	for raceNumber in range(0, len(inputDatas)):

		inputData = inputDatas[raceNumber]
		results.append(0)

		for index in range(0, inputData[0]):

			speed = index

			distance = speed * (inputData[0] - index)

			if(distance > inputData[1]):
				results[raceNumber] += 1

		print(f"Number of Wins {results[raceNumber]}")

	sum = 1

	for result in results:
		sum *= result

	print(f"Sum = {sum}")


def main_part2():

	f = open("input_1.txt", "r")

	# Populate inputs.
	fullInput = f.readlines();

	goalTime = int(fullInput[0].split(':')[1].replace(' ', ''))
	goalDistance = int(fullInput[1].split(':')[1].replace(' ', ''))

	print(f"time={goalTime} distance={goalDistance}")

	# Calculate Results
	result : int = 0
	
	for index in range(0, goalTime):

		speed = index

		distance = speed * (goalTime - index)

		if(distance > goalDistance):
			result += 1

	print(f"Number of Wins = {result}")


def getListOfNumbers(line) -> [int]:

	result = []

	myList = line.split(" ")

	for item in myList:

		if item == "":
			continue

		result.append(int(item))

	return result

if __name__ == "__main__":
	main_part2()