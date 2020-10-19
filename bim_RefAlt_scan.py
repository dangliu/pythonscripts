#!/usr/bin/python3

usage = """
This script is for scanning ref-alt reverse case in one plink format bim file based on another bim file.
It was written by Dang Liu. Last updated: Aug 11 2020.
usage:
python3 bim_RefAlt_scan.py bim1 bim2

"""

# modules here
import sys, re

# if input number is incorrect, print the usage
if len(sys.argv) < 3:
        print(usage)
        sys.exit()


# Read both bim files
# Read them line by line
# Get REF & ALT stored by ID in dictionaries

bim1 = open(sys.argv[1], 'r')
dic1 = {}

line1 = bim1.readline()
while(line1):
	line1_s = re.split(r'\s+', line1)
	ID = line1_s[1]
	Ref = line1_s[4]
	Alt = line1_s[5]
	dic1[ID] = []
	dic1[ID].append(Ref)
	dic1[ID].append(Alt)
	line1 = bim1.readline()
bim1.close()


bim2 = open(sys.argv[2], 'r')
dic2 = {}

line2 = bim2.readline()
while(line2):
	line2_s = re.split(r'\s+', line2)
	ID = line2_s[1]
	Ref = str(line2_s[4])
	Alt = str(line2_s[5])
	dic2[ID] = []
	dic2[ID].append(Ref)
	dic2[ID].append(Alt)
	line2 = bim2.readline()
bim2.close()

# output
out = open("RefAlt.rev.snps", 'w')
out2 = open(sys.argv[1].replace(".bim", ".RefAlt.bim"), 'w')
# Loop for bim1
for ID in dic1:
	ID_s = re.split(r'_', ID)
	if (ID in dic2 and dic1[ID][0] == dic2[ID][1] and dic1[ID][1] == dic2[ID][0]):
		print(ID, end="\n", file=out)
		print(ID_s[0], ID, "0", ID_s[1], dic1[ID][1], dic1[ID][0], sep="\t", end="\n", file=out2)
	elif (ID in dic2 and dic1[ID][0] == "0" and dic1[ID][1] == dic2[ID][0]):
		print(ID, end="\n", file=out)
		print(ID_s[0], ID, "0", ID_s[1], dic1[ID][1], dic1[ID][0], sep="\t", end="\n", file=out2)
	elif (ID in dic2 and dic1[ID][0] == dic2[ID][1] and dic1[ID][1] == "0"):
		print(ID, end="\n", file=out)
		print(ID_s[0], ID, "0", ID_s[1], dic1[ID][1], dic1[ID][0], sep="\t", end="\n", file=out2)
	elif (ID in dic2 and dic2[ID][1] == "0" and dic1[ID][1] == dic2[ID][0]):
		print(ID, end="\n", file=out)
		print(ID_s[0], ID, "0", ID_s[1], dic1[ID][1], dic1[ID][0], sep="\t", end="\n", file=out2)
	elif (ID in dic2 and dic1[ID][0] == dic2[ID][1] and dic2[ID][0] == "0"):
		print(ID, end="\n", file=out)
		print(ID_s[0], ID, "0", ID_s[1], dic1[ID][1], dic1[ID][0], sep="\t", end="\n", file=out2)
	else:
		print(ID_s[0], ID, "0", ID_s[1], dic1[ID][0], dic1[ID][1], sep="\t", end="\n", file=out2)

#last_v20200811
