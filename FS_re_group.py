#!/usr/bin/python3

usage = """
This script is for replacing the IID in <Pop> of the fineSTRUCTURE tree xml output to their Pop/Group + number according to an info file
It was written by Dang Liu. Last updated: Nov 11 2019.
usage:
python3 FS_re_group.py FS.tree.xml info

output:
FS.tree.reG.xml

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
pop_dict = {}

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



# Read FS tree

f2 = open(sys.argv[2], 'r')
prefix = sys.argv[2].replace(".xml","")
out_f = open(prefix + ".reG.xml", "w")
line2 = f2.readline()

# Make a number for each ind
n = 0

while(line2):
        if re.search(r'<Pop>', line2):
                #print(line2)
                line2_s = line2.replace("</Pop>\n","").split("(")
                for i in line2_s:
                        if re.search(r'<Pop>', i):
                                print(i, end= '', file=out_f)
                        elif re.search(r'\,', i):
                                print("(", end= '', file=out_f)
                                i_s = i.split(",")
                                for x in i_s:
                                        n += 1
                                        if re.search(r'\)', x):
                                                print(ind_dict[x.replace(")","")], n, ")", sep="", end= '', file=out_f)
                                        else:
                                                print(ind_dict[x], n, ",", sep="", end= '', file=out_f)
                        else:
                                print("(", end= '', file=out_f)
                                n += 1
                                print(ind_dict[i.replace(")","")], n, ")", sep="", end= '', file=out_f)
                print("</Pop>\n", file=out_f)
        else:
                print(line2, end='', file=out_f)          
        line2 = f2.readline()
f2.close()

out_f.close()
print(prefix + ".reG.xml is output!")





# last_v20210531