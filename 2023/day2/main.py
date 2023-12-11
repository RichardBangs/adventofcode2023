import os



def main():

	f = open("input.txt", "r")

	sum = 0

	fullInput = f.readlines();

	for line in fullInput:

		line = line.strip('\n')
		line = line.replace(' ', '')

		gameNumber = getFirstNumberOnLine(line.split(':')[0])

		resultLine = line.split(':')[-1]

		bagPulls = resultLine.split(';')

		print("\nGame " + str(gameNumber))
		print(line)

		maxCubes = {'green':0, 'blue':0, 'red':0}

		isGameValid = True

		for bagPull in bagPulls:
			print(bagPull)
			dictNumCubes = getNumberOfCubes(bagPull)

			for maxCube in maxCubes:
				if dictNumCubes[maxCube] > maxCubes[maxCube]:
					maxCubes[maxCube] = dictNumCubes[maxCube]

		power = 0

		for maxCube in maxCubes:
			if power == 0:
				power = maxCubes[maxCube]
			else:
				power *= maxCubes[maxCube]

		if isGameValid:
			sum += power

	print("Sum = " + str(sum))



def getFirstNumberOnLine(line):

	result = []

	index = 0

	while(index < len(line)):

		char = line[index]

		# Found a number...
		if(char.isnumeric()):

			numberString = ""

			# Find all digits of the number that are next to each other.
			while (char.isnumeric()):
				
				numberString += char

				index += 1

				if(index >= len(line)):
					break

				char = line[index]

			result.append(int(numberString))

		index += 1

	return result[0]

def getNumberOfCubes(line):

	results = {'green':0, 'blue':0, 'red':0}

	lineSplit = line.split(',')

	print(lineSplit)

	for cube in lineSplit:

		for result in results:

			amount = getFirstNumberOnLine(cube)

			for key in results:

				if result in cube:

					results[result] = amount


	print(results)

	return results




if __name__ == "__main__":
	main()