#!/usr/bin/python3

usage = """
This script is for replacing the IID ChromoPainter output to their Pop/Group + number according to an info file
It was written by Dang Liu. Last updated: Nov 11 2019.
usage:
python3 CP_re_group.py CP.chunkcounts.out info

output:
CP.chunkcounts.reG.out

"""

# modules here
import sys, re
import itertools

# if input number is incorrect, print the usage
if len(sys.argv) < 3:
        print(usage)
        sys.exit()

# Read pop info file

f1 = open(sys.argv[1], 'r')
ind_dict = {}

line = f1.readline() # remove header
line = f1.readline()
while(line):
        line_s = re.split(r'\s+', line)
        IID = line_s[1]
        pop = line_s[2]
        Group = line_s[12]
        ind_dict[IID] = []
        ind_dict[IID] = Group
        #ind_dict[IID] = pop
        line = f1.readline()
f1.close()

print("Ind info processed!")



# Read CP file

pop_dict = {}

f2 = open(sys.argv[2], 'r')
prefix = sys.argv[2].replace(".out","")
out_f = open(prefix + ".reG.out", "w")
line2 = f2.readline()
print(line2, end='', file=out_f) # c factor
line2 = f2.readline()
# Make a number for each ind
col = 0
row = 0

while(line2):
        if re.search(r'Recipient', line2):
                #print(line2)
                line2_s = re.split(r'\s+', line2)
                #print(line2_s[-1]) # the last one is a space element
                #print(line2_s[-2])
                for i in line2_s[:-1]:
                        #print(i)
                        if (i != line2_s[-2]):
                                if re.search(r'Recipient', i):
                                        print(i, end=" ", file=out_f)
                                else:
                                        col += 1
                                        print(ind_dict[i], col, sep='', end=" ", file=out_f)
                        else:
                                col += 1
                                print(ind_dict[i], col, sep='', end="\n", file=out_f)

        else:   
                line2_s = re.split(r'\s+', line2)
                row += 1
                print(ind_dict[line2_s[0]], row, sep='', end=' ', file=out_f)
                print(*line2_s[1:], end='\n', file=out_f) # the * can make a list space-separated
        line2 = f2.readline()
f2.close()

out_f.close()
print(prefix + ".reG.out is output!")





# last_v20210531