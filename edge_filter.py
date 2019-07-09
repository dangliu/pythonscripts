#!/usr/bin/python3

usage = """
This script is for filtering repetitive IBD sharing patterns for network visualization.
It was written by Dang Liu. Last updated: Mar 27 2019.
usage:
python3 edge_filter.py edge.txt

"""

# modules here
import sys, re

# if input number is incorrect, print the usage
if len(sys.argv) < 2:
        print(usage)
        sys.exit()

f1 = open(sys.argv[1], 'r')
pair = []

line = f1.readline()
while(line):
	line_s = re.split(r'\s+', line.replace("\n", ""))
	pop1 = line_s[0]
	pop2 = line_s[1]
	pair1 = pop1 + pop2
	pair2 = pop2 + pop1
	if (pair1 not in pair and pair2 not in pair):
		pair.append(pair1)
		pair.append(pair2)
		print(line.replace("\n",""))
	else:
		pass
	line = f1.readline()
f1.close()