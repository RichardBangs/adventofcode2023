import os



def main():

	f = open("input.txt", "r")

	sum = 0

	fullInput = f.readlines();

	for line in fullInput:
		line = line.strip('\n')

		allNumbers = getAllNumbersOnLine(line)

		firstNumber = allNumbers[0]
		lastNumber = allNumbers[-1]

		print(line)
		print(allNumbers)
		print(str(firstNumber) + " " + str(lastNumber))

		firstDigit = str(firstNumber)[0]
		lastDigit = str(lastNumber)[-1]

		combinedDigits = firstDigit + lastDigit

		sum += int(combinedDigits)

	print("Sum = " + str(sum))
	


# Returns array of numbers as string, example: [4, 6, 76]
#	THIS ISN'T AS NICE AS I WANTED AS WE HAD TO REPEAT CHARACTERS FROM SOME LETTERS, SO IT DOESN'T ACCURATELY SPLIT NUMBERS
#	BUT ITS ENOUGH FOR THE CHALLENGE - a bit annoying...
def getAllNumbersOnLine(line):

	result = []

	numberStrings = {'one':'o1e', 'two':'t2o', 'three':'t3e', 'four':'f4r', 'five':'f5e', 'six':'s6x', 'seven':'s7n', 'eight':'e8t', 'nine':'n9e' }

	index = 0

	line = line.lower()

	for key in numberStrings:
		line = line.replace(key, numberStrings[key])



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

	return result




if __name__ == "__main__":
	main()