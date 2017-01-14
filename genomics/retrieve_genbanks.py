import os
import json
import pprint
import gzip
import re

from ftplib import FTP
from Bio import Entrez
from Bio import SeqIO

# Parameters 
Entrez.email = "clo@kuleuven.be"
NGENOME = 164
NCBI_FTP = "ftp.ncbi.nlm.nih.gov"
FTP_PATH = "/genomes/all/"
sequence_handle= "_genomic.gbff.gz"

# get ID of entries in assembly database
query = "\"Clostridium botulinum\"[ORGN] AND \"complete genome\"[FILTER]" 
handle = Entrez.esearch(db="assembly", term=query, retmax=NGENOME)
record = Entrez.read(handle)
record["IdList"]

# pprint.prrint(Entrez.read(Entrez.esummary(db="assembly", id=790501, report="full")))

# for each assembly, get the summary report first and then the sequence (refseq)
folder_list = []
for asm_id in record["IdList"]:
    summary_handle = Entrez.esummary(db="assembly", id=asm_id, report="full")
    summary = Entrez.read(summary_handle, validate=False)

    # parse for refseq accession number
    refseq = summary['DocumentSummarySet']['DocumentSummary'][0]['AssemblyAccession']
    asm = summary['DocumentSummarySet']['DocumentSummary'][0]['AssemblyName']
    folder_list.append(refseq + "_" + asm)
    
    # saving all xmetadata
    with open(os.path.join("test", refseq + "_" + asm + ".json" ),'w') as f:
        f.write(str(summary['DocumentSummarySet']['DocumentSummary'][0]))

print(folder_list)

# Connection to NCBI FTP
try:
    print("Connection to %s" % NCBI_FTP)
    ftp = FTP(NCBI_FTP)
    ftp.login()
    print("Connected")
except:
    print("Connection issues")
    ftp.quit()

# Fetching over FTP
for folder in folder_list:
    print("Fetching %s" % folder)
    ftp.cwd(FTP_PATH + folder)
    try:
        filename = folder + ".gbff.gz"
        ftp.retrbinary('RETR %s' % folder + sequence_handle, open(os.path.join("test", filename), "wb").write)
    except:
        print("Error fetching file %s - does not exits" % (folder + sequence_handle))
        continue
ftp.quit()

