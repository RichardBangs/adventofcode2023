import os
import sys
import time
import subprocess


# This is a wrapper to run any day's solution in either test or input mode.

# Command Line Arguments:
#	pypy run.py [year] [day] [mode]
#
# Example:
#	pypy run.py "test" 2023 1
#

runMode : str = sys.argv[1]

if(runMode == "test"):
	year = int(sys.argv[2])
	day = int(sys.argv[3])
	part = int(sys.argv[4])

	inputFile = f"{year}/day{day}/test_{part}.txt"

	if not (os.path.exists(inputFile)):
		inputFile = f"{year}/day{day}/test_1.txt"

	assert(os.path.exists(inputFile))

	retVal = subprocess.run(["pypy", f"{year}/day{day}/main.py", f"{part}", inputFile])

	print(f"Test {year}/day{day}")
	print(f"Output = {retVal.returncode}")


if(runMode == "run"):
	year = int(sys.argv[2])
	day = int(sys.argv[3])
	part = int(sys.argv[4])

	inputFile = f"{year}/day{day}/input_{part}.txt"

	if not (os.path.exists(inputFile)):
		inputFile = f"{year}/day{day}/input_1.txt"

	assert(os.path.exists(inputFile))

	subprocess.run(["pypy", f"{year}/day{day}/main.py", f"{part}", inputFile])

	print(f"Run {year}/day{day}")

	print(f"Output = {retVal.returncode}")