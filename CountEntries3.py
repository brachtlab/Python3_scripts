#!/usr/bin/env python
from Bio import SeqIO
from Bio import Seq
from Bio.Seq import Seq
import sys
from sys import argv

seqHandle=open("%s"%argv[1],"r")

i=0
for seq_record in SeqIO.parse(seqHandle, "fasta"):
	i=i+1
	if i%10000==0:
		print("processed %s sequences so far...."%i)

print("there are %s sequences in file."%i)

seqHandle.close()
