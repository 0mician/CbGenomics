import os
import re

from Bio import Entrez
from Bio import SeqIO

Entrez.email = "clo@kuleuven.be"
NSRA = 154

# get ID of entries in SRA database
query = "SRP059342" 
handle = Entrez.esearch(db="sra", term=query, retmax=NSRA)
record = Entrez.read(handle)
record["IdList"]

sra_list = []
for sra_id in record["IdList"]:
    # get strain name
    summary_handle = Entrez.elink(dbfrom="sra", id=sra_id, db="biosample")
    summary = Entrez.read(summary_handle, validate=False)
    id_biosample = summary[0]['LinkSetDb'][0]['Link'][0]['Id']

    biosample = Entrez.esummary(db="biosample", id=id_biosample, report="summary")
    summary_bs = Entrez.read(biosample)
    
    strain = summary_bs['DocumentSummarySet']['DocumentSummary'][0]['Infraspecies']
    
    # get SRR
    pattern = re.compile('SRR[0-9]*')
    sra_handle = Entrez.esummary(db="sra", id=sra_id, report="summary")
    sra_summary = Entrez.read(sra_handle, validate=False)
    run_xml = sra_summary[0]['Runs']
    run = re.findall(pattern, run_xml)[0]
    
    # saving to file
    with open(os.path.join("data", "strains_run_dictionary.txt"), "a") as f:
        f.write(str(strain)+","+str(run)+"\n")
