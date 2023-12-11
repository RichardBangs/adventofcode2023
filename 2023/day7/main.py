import os
import time



def main_part1():

	hands : [(int, int)] = []

	f = open("input_1.txt", "r")

	# Populate inputs.
	fullInput1 = f.readlines();

	for line in fullInput1:

		line = line.strip('\n')

		if(line == ""):
			continue

		hand = line.split(' ')[0]
		bet = line.split(' ')[1]

		score = scoreHand(hand)
		hands.append((score, int(bet)))

	sortedHands = sorted(hands)

	sum = 0

	for index in range(0, len(sortedHands)):
		sum += sortedHands[index][1] * (index+1)

	print(f"Result = {sum}")


def getNumberSame(hand):

	sortedHand : [char] = []
	for char in hand:
		sortedHand.append(char)
	sortedHand.sort()

	max = 0
	current = 0

	for index in range(1, len(sortedHand)):
		if(sortedHand[index] == sortedHand[index-1]):
			current += 1
		else:
			current = 0

		if(current > max):
			max = current

	return max+1


def getNumberPairs(hand):

	sortedHand : [char] = []
	for char in hand:
		sortedHand.append(char)
	sortedHand.sort()

	current = 0
	pairs = 0

	for index in range(1, len(sortedHand)):

		if(sortedHand[index] == sortedHand[index-1]):
			current += 1
		else:
			if(current >= 1):
				pairs += 1

			current = 0

	if(current >= 1):
		pairs += 1

	return pairs

def getHighCardValue(hand) -> int:

	handSize = len(hand)

	sum = 0
	for index in range(0, handSize):

		value = 1
		match(hand[index]):
			case '2':	value = 2
			case '3':	value = 3
			case '4':	value = 4
			case '5':	value = 5
			case '6':	value = 6
			case '7':	value = 7
			case '8':	value = 8
			case '9':	value = 9
			case 'T':	value = 10
			case 'J':	value = 11
			case 'Q':	value = 12
			case 'K':	value = 13
			case 'A':	value = 14

		inc = value * (pow(16, (handSize-index)-1))

		sum += inc

	assert True
	return sum


def scoreHand(hand) -> [int]:

	highCard = getHighCardValue(hand)
	maxSame = getNumberSame(hand)
	
	match(maxSame):
		case 5:		return 1000000000+highCard
		case 4:		return 900000000+highCard

	if(maxSame == 3):
		if(getNumberPairs(hand) == 2):
			return 700000000+highCard
		else:
			return 600000000+highCard

	if(maxSame == 2):
		if(getNumberPairs(hand) == 2):
			return 500000000+highCard
		else:
			return 400000000+highCard

	return 0+highCard


def main_part2():

	hands : [(int, int)] = []

	f = open("input_1.txt", "r")

	# Populate inputs.
	fullInput1 = f.readlines();

	for line in fullInput1:

		line = line.strip('\n')

		if(line == ""):
			continue

		hand = line.split(' ')[0]
		bet = line.split(' ')[1]


		score = findMaxScoreWithJoker(hand, 0) + getHighCardValue2(hand)
		hands.append((score, int(bet)))

	sortedHands = sorted(hands)

	sum = 0

	for index in range(0, len(sortedHands)):
		sum += sortedHands[index][1] * (index+1)

	print(f"Result = {sum}")


def getHighCardValue2(hand) -> int:

	handSize = len(hand)

	sum = 0
	for index in range(0, handSize):

		value = 1
		match(hand[index]):
			case '2':	value = 2
			case '3':	value = 3
			case '4':	value = 4
			case '5':	value = 5
			case '6':	value = 6
			case '7':	value = 7
			case '8':	value = 8
			case '9':	value = 9
			case 'T':	value = 10
			case 'J':	value = 1
			case 'Q':	value = 12
			case 'K':	value = 13
			case 'A':	value = 14

		inc = value * (pow(16, (handSize-index)-1))

		sum += inc

	assert True
	return sum

def replace_by_index(string, idx, character):
    return string[:idx] + character + string[idx+1:]

def findMaxScoreWithJoker(hand : str, startChar : int) -> [int]:

	handSize = len(hand)

	replacements = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

	maxScore = scoreHand2(hand)

	if(maxScore == 1000000000):
		return maxScore

	if(maxScore == 900000000 and 'J' in hand):
		return 1000000000

	for index in range(startChar, handSize):
		if(hand[index] == 'J'):
			for replacement in replacements:
				newHand = replace_by_index(hand, index, replacement)

				score = findMaxScoreWithJoker(newHand, index+1)

				if(score > maxScore):
					maxScore = score

				score2 = scoreHand2(newHand)

				if(score2 > maxScore):
					maxScore = score2

	return maxScore


def scoreHand2(hand) -> [int]:

	maxSame = getNumberSame(hand)
	
	match(maxSame):
		case 5:		return 1000000000
		case 4:		return 900000000
		case 3:
			if(getNumberPairs(hand) == 2):
				return 700000000
			else:
				return 600000000
		case 2:
			if(getNumberPairs(hand) == 2):
				return 500000000
			else:
				return 400000000

	return 0


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
	print("Day 7 - Timings")

	for index in range(0, len(name)):
		print (f"{name[index]}{((end[index]-start[index])*1000):,.2f}ms")
