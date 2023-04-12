#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv

#usage: ./get_subset_transcripts_from_genes.py all_transcripts.fasta stringtie_merged.gtf upregulated/downregulated.txt (delinated by newlines, one gene per line, gene names)

transcript_handle=open("%s"%argv[1],"r")
outHandle=open("%s.fasta"%argv[3],'w')
gtf_handle=open('%s'%argv[2],'r')
updownHandle=open('%s'%argv[3],'r')
tid='empty'
gname='unused'
newstring='unused'
dict={}
x=0
j=0
#----------get genes and transcripts from gtf file---------------------#
for line in gtf_handle:
	for item in line.split('\t'):
		for thing in item.split(';'):
			if ('gene_id' in thing)and (not 'ref' in thing):
				gname=thing.split(' ')[1].strip('"')
			if 'transcript_id' in thing:
				#print(thing.split(' '))
				tid=thing.split(' ')[2].strip('"')
	if gname in dict.keys():
		old=dict[gname]
		if tid != old:
			x+=1
			newstring='%s;%s'%(old,tid)
			dict[gname]=newstring
	else:
		j+=1
		dict[gname]=tid
	
print('found %s genes and associated transcripts in gtf file'%len(dict))
# ------get up and downreg genes, figure corresponding transcripts --------#
transDict={}#will store transcripts
u=0
t=0
for line in updownHandle:
	name=line.split()[0]
	if '|' in name:
		start=name.split('|')[0]
		name=start
	u+=1
	if name in dict.keys():
		if ';' in dict[name]: #has multiple transcripts
			list=dict[name].split(';')
			for tr in list:
				t+=1
				transDict[tr]=1
		else:#single transcript
			t+=1
			transDict[dict[name]]=1
			
	else:
		print("missing a transcript? %s"%name)

print('found %s transcripts coming from %s genes'%(len(transDict),u))
print(transDict)

#-----------get transcripts from fasta-----------#
records=[]
v=0
for seq_record in SeqIO.parse(transcript_handle,'fasta'):
	if seq_record.id in transDict.keys():
		records.append(seq_record)
		v+=1
		del transDict[seq_record.id] #remove the record
SeqIO.write(records,outHandle,'fasta')
print('found and wrote %s transcripts to file.'%v)
print('%s transcripts not found and written: %s'%(len(transDict),transDict))
print('see your output file %s.fasta for your data!'%argv[3])
transcript_handle.close()
outHandle.close()
gtf_handle.close()
updownHandle.close()
