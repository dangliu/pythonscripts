#!/usr/bin/python3

usage = """
This script is for combining refined-IBD output with poppualtion information and calculate the descriptive statistics.
It was written by Dang Liu. Last updated: Mar 11 2019.
usage:
python3 IBD_stats.py pop.info merged.ibd

"""

# modules here
import sys, re, math

# if input number is incorrect, print the usage
if len(sys.argv) < 3:
        print(usage)
        sys.exit()


# Define function
def median(lst):
	sort_list = sorted(lst)
	lst_length = len(lst)
	if lst_length%2 == 0:
		m = (sort_list[int(lst_length/2-1)] + sort_list[int(lst_length/2)])/2
	else:
		m = sort_list[int((lst_length-1)/2)]
	return m
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys 

# Read pop info file

f1 = open(sys.argv[1], 'r')
ind_dict = {}
pop_dict = {}

line = f1.readline() # remove header
line = f1.readline()
while(line):
	line_s = re.split(r'\s+', line)
	IID = line_s[1]
	pop = line_s[2]
	country = line_s[4]
	ind_dict[IID] = pop
	if (pop not in pop_dict):
		pop_dict[pop] = {}
		pop_dict[pop]["Country"] = country
	line = f1.readline()
f1.close()

#print(pop_dict)

# Make la start point to count number and length of sharing IBD for each pop vs. pop pair 
for i in pop_dict:
	for k in pop_dict:
		pop_dict[i][k] = {}
		pop_dict[i][k]["L"] = []
		pop_dict[i][k]["N"] = 0
print("pop info processed!")
#print(pop_dict)
# Read in IBD file

# Output a reformatted IBD result with population informations
out_f = open("Merged.pop.ibd", "w")

f2 = open(sys.argv[2], 'r')
ibd_dict = {}
line2 = f2.readline()
while(line2):
	line2_s = re.split(r'\s+', line2.replace("\n",""))
	ind1 = line2_s[0]
	ind2 = line2_s[2]
	chro = line2_s[4]
	len1 = int(line2_s[6]) - int(line2_s[5]) # Mb
	len2 = line2_s[8] # cM
	LOD = line2_s[7]
	print(ind1, ind_dict[ind1], ind2, ind_dict[ind2], chro, len1, len2, LOD, sep="\t", end="\n", file=out_f)
	pop_dict[ind_dict[ind1]][ind_dict[ind2]]["L"].append(float(len2)) # Use cM as sharing length count
	pop_dict[ind_dict[ind1]][ind_dict[ind2]]["N"] += 1 # Count sharing number between pop1 and pop2
	line2 = f2.readline()
f2.close()

out_f.close()
print("Merged.pop.ibd is output!")
# Stats

# Output stats
out_f2 = open("Merged.pop.ibd.stats", "w")
out_f3 = open("Merged.pop.ibd.within.len", "w")

# Headers
print("Pop1", "Pop2", "Total" ,"Average", "Median", "N", "N_ind", "Country1" ,"Country2", sep="\t", end="\n", file=out_f2)
print("Pop", "Length", "N_ind", "Country", sep="\t", end="\n", file=out_f3)

for i in pop_dict:
	print("Processing population " + i + "...")
	for k in pop_dict[i]:
		if (k != "Country"):
			N = pop_dict[i][k]["N"]
			N_ind = math.ceil(pop_dict[i][k]["N"]/len(getKeysByValue(ind_dict, i))) # normalized by pop1 sample size here
			Country1 = pop_dict[i]["Country"]
			Country2 = pop_dict[k]["Country"]
			if (i == k):
				for l in pop_dict[i][k]["L"]:
					print(i, l, N_ind, Country1, sep="\t", end="\n", file=out_f3) # Output in within stats if pop1 == pop2
			if (N != 0):
				Total = "%.3f" % (sum(pop_dict[i][k]["L"]))
				Average = "%.3f" % (sum(pop_dict[i][k]["L"])/len(pop_dict[i][k]["L"]))
				Median = "%.3f" %  (median(pop_dict[i][k]["L"]))
				print(i, k, Total, Average, Median, N, N_ind, Country1, Country2, sep="\t", end="\n", file=out_f2)
			else:
				print(i, k, "NA", "NA", "NA", "NA", "NA", Country1, Country2, sep="\t", end="\n", file=out_f2) # Put NA for no sharing

out_f2.close()
out_f3.close()

print("Merged.pop.ibd.stats is output!")
print("Merged.pop.ibd.within.len is output!")
print("All done!")

