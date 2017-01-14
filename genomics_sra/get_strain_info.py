import os

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
    summary_handle = Entrez.elink(dbfrom="sra", id=sra_id, db="biosample")
    summary = Entrez.read(summary_handle, validate=False)
    id_biosample = summary[0]['LinkSetDb'][0]['Link'][0]['Id']

    biosample = Entrez.esummary(db="biosample", id=id_biosample, report="summary")
    summary_bs = Entrez.read(biosample)
    
    # parse for sra entry and strain name
    sra = summary_bs['DocumentSummarySet']['DocumentSummary'][0]['Identifiers']
    strain = summary_bs['DocumentSummarySet']['DocumentSummary'][0]['Infraspecies']
    
    # saving to file
    with open(os.path.join("data", "strains.txt"), "a") as f:
        f.write(str(strain)+"||"+str(sra)+"\n")

