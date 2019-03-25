#!/usr/bin/python3

usage = """
This script is for filtering refined-IBD output based on to-be-removed individual list.
It was written by Dang Liu. Last updated: Mar 22 2019.
usage:
python3 IBD_filter.py remove.ind merged.ibd

"""

# modules here
import sys, re, math

# if input number is incorrect, print the usage
if len(sys.argv) < 3:
        print(usage)
        sys.exit()

 # Read remove.ind file

f1 = open(sys.argv[1], 'r')

remove_ind = []

line = f1.readline()
while(line):
	line_s = re.split(r'\s+', line.replace("\n",""))
	IID = line_s[1]
	remove_ind.append(IID)
	line = f1.readline()
f1.close()

# Output a reformatted IBD result with population informations
out_f = open(sys.argv[2] + ".filtered", "w")

f2 = open(sys.argv[2], 'r')
line2 = f2.readline()
while(line2):
	line2_s = re.split(r'\s+', line2.replace("\n",""))
	ind1 = line2_s[0]
	ind2 = line2_s[2]
	if (ind1 not in remove_ind and ind2 not in remove_ind):
		print(line2.replace("\n",""), file=out_f)
	line2 = f2.readline()
f2.close()
out_f.close()

# last_v 20190322