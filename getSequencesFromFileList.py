#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
#getContigs.py <assemblyfile> <textfile_delimited_by_\n>
scafHandle=open('%s'%argv[2],'r')
outHandle=open("%s.fasta"%argv[2],'w')
genome_handle=open("%s"%argv[1],"r")
scafDict={}
x=0
for line in scafHandle:
	x+=1
	scafDict[line.rstrip('\n')]=1
#print scafDict
j=0
for seq_record in SeqIO.parse(genome_handle,"fasta"):
	seqlength=len(seq_record.seq)
	ident="%s"%seq_record.id
	if ident in scafDict.keys():
		j+=1
		outHandle.write(">%s\n%s\n"%(ident,seq_record.seq))
		print("found %s"%ident)
print('%s of %s sequences found and printed to file.'%(j,x))
		
genome_handle.close()
outHandle.close()
