#!/usr/bin/python3

usage = """
This script is for calculating mean and SE for each pop/ancient sample in top XX runs of ADMIXTURE results at specific K 
It was written by Dang Liu. Last updated: Feb 02 2020.
usage:
python3 ADMIXTURE_stats.py pong_ind2pop.txt pong_filemap.TopXX.KX 

output:
pong_filemap.TopXX.KX.stats

"""

# modules here
import sys, re, math, statistics
from scipy.stats import sem
import numpy as np


# if input number is incorrect, print the usage
if len(sys.argv) < 3:
        print(usage)
        sys.exit()

# Read the ind to pop file
# Save it into a list
with open(sys.argv[1]) as f0:
    ind2pop = f0.read().splitlines()

#print(ind2pop)

# Create a dictionary to collect info
dic = {}

# Save number of K
K_n = 0

# Read the file map
f1 = open(sys.argv[2], 'r')

top_n = 1
line = f1.readline()
while(line):	
	line_s = re.split(r'\s+', line)
	PATH = line_s[2]
	print("Reading " + PATH)
	Q = open(PATH, 'r')
	lineQ = Q.readline()
	line_n = 0
	while(lineQ):
		pop = ind2pop[line_n]
		#print(pop)
		if (pop not in dic):
			dic[pop] = {}
			IND_n = line_n + 1
			dic[pop][IND_n] = {}
			lineQ_s = re.split(r'\s+', lineQ.replace("\n",""))
			sort_Q = sorted([float(i) for i in lineQ_s])
			K_n = len(sort_Q)
			dic[pop][IND_n][top_n]=sort_Q
		else:
			IND_n = line_n + 1
			if (IND_n not in dic[pop]):	
				dic[pop][IND_n] = {}	
				lineQ_s = re.split(r'\s+', lineQ.replace("\n",""))
				sort_Q = sorted([float(i) for i in lineQ_s])
				dic[pop][IND_n][top_n]=sort_Q
			else:
				lineQ_s = re.split(r'\s+', lineQ.replace("\n",""))
				sort_Q = sorted([float(i) for i in lineQ_s])
				dic[pop][IND_n][top_n]=sort_Q				
		line_n += 1
		lineQ = Q.readline()
	Q.close()
	top_n += 1
	line = f1.readline()
f1.close()

print("All info collected!")
#print(dic)


# Make another dictionary with pop as key
dic2 = {}
for pop in ind2pop:
	if pop not in dic2:
		dic2[pop] = {}

for pop in dic2:
	for i in range(1, K_n+1):
		dic2[pop][i] = []

# Collect the Q by K for each pop / ancient sample
for pop in dic:
	for IND_n in dic[pop]:
		for top_n in dic[pop][IND_n]:
			for i in range(0, K_n):
				dic2[pop][i+1].append(dic[pop][IND_n][top_n][i])


print("Q of each pop has been collected and sorted by Ks!")

# Output the mean and SE for each pop's ADMIXTURE Q sorted by their values
out_f1 = open(sys.argv[2] + ".stats", "w")
for pop in dic2:
	print(pop, end="\t", file=out_f1)
	print(pop)
	for i in range(1, K_n+1):
		mean = "%.1f" % (statistics.mean(dic2[pop][i])*100)
		stderr = "%.1f" % (sem(dic2[pop][i])*100)
		variance = "%.1f" % (np.var(dic2[pop][i])*100)
		print(mean, stderr, variance, sep=", ", end="\t", file=out_f1)
		print(dic2[pop][i])
	print("\n", end="", file=out_f1)

print("All done! " + sys.argv[2] + ".stats is output!")



# last_v20200203