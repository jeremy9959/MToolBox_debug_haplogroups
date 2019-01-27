#!/usr/bin/env python



import getopt, sys, re, os, glob, csv
from classifier import tree, NGclassify, consts, datatypes, parse_mhcs
from bioinf.seqs import SeqList
import io_modules.csv
import io_modules.old_table
import io_modules.serialize
import pandas as pd
import os.path
sys.setrecursionlimit(100000)


csvfile,out_fname = sys.argv[1:]


#write pickle file for MToolBox
tree_file = csv.reader(open(csvfile, 'rb'))

pickle_fname = csvfile + '.pickle'
aplo_list = io_modules.csv.parse_csv(tree_file)
htree = tree.HaplogroupTree(aplo_list=aplo_list)
pickle_file = open(pickle_fname, 'wb')
pickle_file.write(htree.serialize())
pickle_file.close()

#write out alleles and haplogroups defined for HmtDB in csv file
pickle_file = pickle_fname
out_file = out_fname + '.csv'
htree = tree.HaplogroupTree(pickle_data=open(pickle_file, 'rb').read())
fh = csv.writer(open(out_file, 'wb'))
for haplo_name in htree:
	io_modules.old_table.write_haplogroup(fh, '', htree[haplo_name])



#write haplogrups.txt tab delimited file for MToolBox
out_file2 = out_fname + '.txt'
hap_file = pd.read_csv(out_file,sep=',',header=None)
subset = hap_file[[0,1,3]]
subset.dropna(inplace=True)
alleles = subset[1].astype(str).str.cat(subset[3])
subset.insert(1,'Allele',alleles)
subset = subset[[0,'Allele']]
subset.columns=['haplogroup_code','POSITIONnucleotidic_change']
subset.to_csv(out_file2,sep='\t',header=True,index=None)

