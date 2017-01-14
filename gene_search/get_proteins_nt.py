import os
import json
import pprint
from textwrap import wrap

from Bio import Entrez
from Bio import SeqIO
from Bio.Alphabet import generic_rna

Entrez.email = "clo@kuleuven.be"
proteins_list = os.path.join("data", "proteins.txt")
fasta_out = os.path.join("data", "spore_proteins.fasta")
proteins_not_found_out = os.path.join("data", "proteins_not_found.txt")

fasta_fh = open(fasta_out, "w") # file handler for output genes (fasta)
proteins_not_found_fh = open(proteins_not_found_out, "w")

with open(proteins_list, "r") as proteins_fh:
    for protein in proteins_fh:
        
        # search first in gene database to get a list of ID
        protein_handle = Entrez.esearch(db="protein", term=protein.strip("\n"))
        protein_record = Entrez.read(protein_handle)
        protein_id_list = protein_record['IdList']

        # any results?
        if(protein_id_list):

            # go through each ID and get linked genome and genomic region
            for protein_id in protein_id_list:
                pr_h = Entrez.efetch(db="protein", id=protein_id, rettype="fasta")
                pr = SeqIO.read(pr_h, "fasta")
                print(pr.description)
                fasta_fh.write(">" + protein.strip("\n") + "@" + pr.description + "\n")
                fasta_fh.write("\n".join(wrap(str(pr.seq), 80)) + "\n")


        # empty list (based on gene label, no results could be found, literature)
        else:
            proteins_not_found_fh.write(protein.strip("\n"))

proteins_fh.close()
proteins_not_found_fh.close()
fasta_fh.close()

#### For the 3 proteins not found, manually looked up NCBI
# ADT22_15425 - not working (gene disrupted)
# nt_handle = Entrez.efetch(db="nucleotide",
#                           id="LHUM01000052.1",
#                           rettype="fasta")
#                           #strand=2,
#                           #seq_start=10637,
#                           #seq_stop=10933)
# nt_record = SeqIO.read(nt_handle, "fasta")
# print(nt_record.seq[10636:10933])
