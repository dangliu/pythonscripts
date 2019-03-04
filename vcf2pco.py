#!/usr/bin/python3

usage = """
This script is for transformating vcf file of diploid samples to spco_ira.r input.
It was written by Dang Liu. Last updated: Nov 02 2018.
usage:
python vcf2pco.py vcf

"""

# modules here
import sys, re

# if input number is incorrect, print the usage
if len(sys.argv) < 2:
        print(usage)
        sys.exit()

# input vcf file
vcf = open(sys.argv[1], 'r')
# output txt file
out_f = open(sys.argv[1].replace('vcf', 'pco.txt'), 'w')

# collections
geno_dit = {'0/0':'-1', '1/0':'0', '0/1':'0', '1/1':'1', './.':'NA'}
k = 0
# processing here
line = vcf.readline()
while(line):
        # get rid of comments
        if ('##' in line):
                pass
        # record sample id
        elif ('#' in line):
                line_s = re.split(r'\s+', line.replace('#', '').replace('\n+', ''))
                l = len(line_s)
                snp_ID_col = line_s[2]
                out_f.write(snp_ID_col + "\t")
                sample_id = line_s[9:l-1]
                #print(sample_id)
                l_s_id = len(sample_id)
                print(l_s_id)
                for i in range(0, l_s_id):
                        if (i != l_s_id-1):
                                out_f.write(sample_id[i] + "\t")
                        else:
                                out_f.write(sample_id[i] + "\n")
        # record genotype
        else:
                k += 1
                print('process ' + str(k) + ' loci...')
                line_s = re.split(r'\s+', line.replace('\n+', ''))
                l = len(line_s)
                snp_id = line_s[2]
                out_f.write(snp_id + "\t")
                genotype = line_s[9:l-1]
                l_g_id = len(genotype)
                for i in range(0, l_g_id):
                        geno = re.sub(r':[-:,.0-9]*', '', genotype[i])
                        if (i != l_g_id-1):
                                out_f.write(geno_dit[geno] + "\t")
                        else:
                                out_f.write(geno_dit[geno] + "\n")  
        line = vcf.readline()
vcf.close()
out_f.close()

print(sys.argv[1].replace('vcf', 'pco.txt') + ' is output.')
print('All done!')



#last_v20181102
