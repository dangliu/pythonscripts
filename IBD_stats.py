#!/usr/bin/python3

usage = """
This script is for combining refined-IBD output with poppualtion information and calculate the descriptive statistics.
It was written by Dang Liu. Last updated: Nov 11 2019.
usage:
python3 IBD_stats.py pop.info merged.ibd

output:
Merged.pop.ibd, Merged.pop.ibd.stats and Merged.pop.ibd.L.N

"""

# modules here
import sys, re, math
import itertools

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
	ind_dict[IID] = []
	ind_dict[IID] = pop
	if (pop not in pop_dict):
		pop_dict[pop] = {}
		# pop_dict[pop]["Country"] = country
	line = f1.readline()
f1.close()

print("Ind info processed!")

# Make a start point to count number and length of sharing IBD for each pop vs. pop pair 
for i in pop_dict:
	for k in pop_dict:
		pop_dict[i][k] = {}
		pop_dict[i][k]["L"] = []
		pop_dict[i][k]["N"] = []
print("pop info processed!")

# Read in IBD file

# Output a reformatted IBD result with population informations
out_f = open(sys.argv[2] + ".pop", "w")
pair_dit = {}

f2 = open(sys.argv[2], 'r')
line2 = f2.readline()
while(line2):
	line2_s = re.split(r'\s+', line2.replace("\n",""))
	ind1 = line2_s[0]
	ind1_id = line2_s[1]
	ind2 = line2_s[2]
	ind2_id = line2_s[3]
	pair = ind1 + ":" + ind2
	chro = line2_s[4]
	start = line2_s[5]
	end = line2_s[6]
	len1 = int(end) - int(start) + 1 # Mb
	len2 = line2_s[8] # cM
	LOD = line2_s[7]
	print(ind1, ind1_id, ind_dict[ind1], ind2, ind2_id, ind_dict[ind2], chro, start, end, LOD, len2, sep="\t", end="\n", file=out_f)
	# Because each ind vs ind just appear once, so need to count it for both pop
	if (pair not in pair_dit):
		pair_dit[pair] = {}
		pair_dit[pair]["L"] = 0
		pair_dit[pair]["N"] = 0
		pair_dit[pair]["L"] += float(len2) # Use cM as sharing length count, count the total IBD length in this pair
		pair_dit[pair]["N"] += 1 # Count total sharing number in this pair
	else:
		pair_dit[pair]["L"] += float(len2)
		pair_dit[pair]["N"] += 1		
	line2 = f2.readline()
f2.close()

out_f.close()
print(sys.argv[2] + ".pop is output!")

# Manage ind pair to pop scale info
for p in pair_dit:
	ind1 = p.split(":")[0]
	ind2 = p.split(":")[1]
	pop1 = ind_dict[ind1]
	pop2 = ind_dict[ind2]
	# Because each ind vs ind just appear once, so need to count it for both pop
	pop_dict[pop1][pop2]["L"].append(pair_dit[p]["L"])
	pop_dict[pop1][pop2]["N"].append(pair_dit[p]["N"])
	pop_dict[pop2][pop1]["L"].append(pair_dit[p]["L"])
	pop_dict[pop2][pop1]["N"].append(pair_dit[p]["N"])	

# Stats

# Output stats
out_f2 = open(sys.argv[2] + ".stats", "w")
out_f3 = open(sys.argv[2] + ".L.N", "w")

# Headers
# print("Pop1", "Pop2", "Total" ,"Average", "Median", "N", "N_ind", "Country1" ,"Country2", sep="\t", end="\n", file=out_f2)
# print("Pop1", "Pop2", "Length", "N_ind", "Country1", "Country2", sep="\t", end="\n", file=out_f3)
print("Pop1", "Pop2", "Total" ,"Average", "Median", "N", "N_ind", sep="\t", end="\n", file=out_f2)
print("Pop1", "Pop2", "Length", "N_ind", sep="\t", end="\n", file=out_f3)


for i in pop_dict:
	print("Processing population " + i + "...")
	for k in pop_dict[i]:
		N = sum(pop_dict[i][k]["N"])
		if (N != 0):				
			#N_ind = round(sum(pop_dict[i][k]["N"])/len(pop_dict[i][k]["N"])) # average sharing number in each pair between the two pops
			all_pair_n = (len(getKeysByValue(ind_dict,i)) * len(getKeysByValue(ind_dict,k)))
			N_ind = "%.3f" % (sum(pop_dict[i][k]["N"]) / all_pair_n) # average sharing number by total possible pairs between the two pops
			Total = "%.3f" % (sum(pop_dict[i][k]["L"]))
			#Average = "%.3f" % (sum(pop_dict[i][k]["L"])/len(pop_dict[i][k]["L"]))
			Average = "%.3f" % (sum(pop_dict[i][k]["L"]) / all_pair_n)
			N0_to_add = all_pair_n-len(pop_dict[i][k]["L"]) # For counting median, we have to know how many more possible pairs but 0 IBD detected should be added
			# print(N0_to_add) # There are some negative values need to fix
			N0_to_add_l = list(itertools.chain.from_iterable(itertools.repeat(x, N0_to_add) for x in [0]))
			Median = "%.3f" %  (median(pop_dict[i][k]["L"] + N0_to_add_l))
			print(i, k, Total, Average, Median, N, N_ind, sep="\t", end="\n", file=out_f2)
			index = 0
			for l in pop_dict[i][k]["L"]:
				print(i, k, l, pop_dict[i][k]["N"][index], sep="\t", end="\n", file=out_f3)
				index += 1 
		else:
			print(i, k, "NA", "NA", "NA", "NA", "NA", sep="\t", end="\n", file=out_f2) # Put NA for no sharing
			for l in pop_dict[i][k]["L"]:
				print(i, k, "NA", "NA", sep="\t", end="\n", file=out_f3) # Put NA for no sharing
'''
		if (k != "Country"):
			N = sum(pop_dict[i][k]["N"])
			Country1 = pop_dict[i]["Country"]
			Country2 = pop_dict[k]["Country"]
			if (N != 0):				
				N_ind = round(sum(pop_dict[i][k]["N"])/len(pop_dict[i][k]["N"])) # average sharing number in each pair between the two pops
				Total = "%.3f" % (sum(pop_dict[i][k]["L"]))
				Average = "%.3f" % (sum(pop_dict[i][k]["L"])/len(pop_dict[i][k]["L"]))
				Median = "%.3f" %  (median(pop_dict[i][k]["L"]))
				print(i, k, Total, Average, Median, N, N_ind, Country1, Country2, sep="\t", end="\n", file=out_f2)
				index = 0
				for l in pop_dict[i][k]["L"]:
					print(i, k, l, pop_dict[i][k]["N"][index], Country1, Country2, sep="\t", end="\n", file=out_f3)
					index += 1 
			else:
				print(i, k, "NA", "NA", "NA", "NA", "NA", Country1, Country2, sep="\t", end="\n", file=out_f2) # Put NA for no sharing
				for l in pop_dict[i][k]["L"]:
					print(i, k, "NA", "NA", Country1, Country2, sep="\t", end="\n", file=out_f3) # Put NA for no sharing
'''
out_f2.close()
out_f3.close()

print(sys.argv[2] + ".stats is output!")
print(sys.argv[2] + ".L.N is output!")
print("All done!")

# last_v20190319, add start and end to Merged.pop.ibd
# last_v20190406, change output naming way
# last_v20191111, remove 'Country' parts
# last_v20200703, average sharing number/length by total possible pairs between the two pops
