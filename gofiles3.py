#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv

#format ipscan.tsv into an association file and names file for GOATools. Writes a population and association files. Requires Python3. Usage: ./gofiles3.py ipscan.tsv 

ipscanhandle=open("%s"%argv[1],"r")
outnames=open("population.txt","w")
outass=open("association.txt","w")
annotDict={}
noannotDict={}
for line in ipscanhandle:
	items=line.split()
	gene_name=items[0]
	go='empty'
	for item in items:
		if item[:3]=='GO:':
			if '|' in item:
				go=item.replace('|',';')
			else:
				go=item
	if go != 'empty':#found annotations
		if gene_name in annotDict.keys():
			oldstring=annotDict[gene_name]
			if go in oldstring:
				pass
			else:
				annotDict[gene_name]=oldstring+';'+go
		else:
			annotDict[gene_name]=go
	else:#no annotations
		noannotDict[gene_name]=1 #store the name

for hgene in annotDict.keys(): #write annotated ones
	outnames.write('%s\n'%(hgene))
	outass.write('%s\t%s\n'%(hgene,annotDict[hgene]))
for gene in noannotDict.keys():
	outnames.write('%s\n'%gene)
ipscanhandle.close()
outnames.close()
outass.close()
