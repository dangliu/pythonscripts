#!/usr/bin/python3

usage = """
This script is for turning the last column of plink fam file into a categorical label (e.g. pop or a/m/md).
It was written by Dang Liu. Last updated: Feb 08 2019.
usage:
python3 fam_label.py info fam

"""

# modules here
import sys, re

# if input number is incorrect, print the usage
if len(sys.argv) < 3:
        print(usage)
        sys.exit()


# Read info file
# Foramt: FID\tIID\tlabel...

info = open(sys.argv[1], 'r')
info_dit = {}

# Read it line by line
line = info.readline()
while(line):
	line_s = re.split(r'\s+', line)
	IID = line_s[1]
	label = line_s[2]
	info_dit[IID] = label
	line = info.readline()
info.close()

# Read fam file

fam = open(sys.argv[2], 'r')
line = fam.readline()
while(line):
	line_s = re.split(r'\s+', line.replace("\n", ""))
	IID = line_s[1]
	print(*line_s[0:-1], info_dit[IID], sep=" ")
	line = fam.readline()
fam.close()

# All done!