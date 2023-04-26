#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
#run this way: getProteins.py <proteinListHandle> <protein fasta>
protein_handle=open("%s"%argv[2],"r")
proteinListHandle=open("%s"%argv[1],'r')
outHandle=open('%s.fasta'%argv[1],'w')

#-----------here, we put protein names into dictionary--------

nameDict={}

for line in proteinListHandle:
	name=line.split()[0]
	#print(name)
	if name in nameDict.keys():
		print('found duplicate! %s'%name)
	else:
		nameDict[name]=1

print('name dictionary is:')
print(nameDict)




#---------below, we search the fasta file for matches to the name dictionary----------	



keys=nameDict.keys()
found=[]
records=[]
x=0
j=0
for seq_record in SeqIO.parse(protein_handle, "fasta"):
	x+=1
	id=seq_record.id
	if id in keys:
		records.append(seq_record)
		found.append(id)
		j+=1
	else:
		descriptionlist=seq_record.description.split(' ')
		for d in descriptionlist:
			#print(d)
			if 'locus=' in d:
				dnew=d.split('locus=')[1]
				print(dnew)
				for k in keys:
					if dnew==k:
						records.append(seq_record)
						found.append(dnew)
						j+=1

SeqIO.write(records,outHandle,"fasta")
print("found:")
print(found)
print("scanned %s and found %s sequences and written to file."%(x,j))
protein_handle.close()
outHandle.close()
proteinListHandle.close()
