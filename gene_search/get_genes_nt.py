import os
import json
import pprint
from textwrap import wrap

from Bio import Entrez
from Bio import SeqIO

Entrez.email = "clo@kuleuven.be"
fasta = "genes_nt.fasta"
gene_list = os.path.join("data", "genes.txt")
fasta_out = os.path.join("data", "genes.fasta")
genes_not_found_out = os.path.join("data", "genes_not_found.txt")

fasta_fh = open(fasta_out, "w") # file handler for output genes (fasta)
genes_not_found_fh = open(genes_not_found_out, "w")

with open(gene_list, "r") as gene_fh:
    for gene in gene_fh:
        
        # search first in gene database to get a list of ID
        gene_handle = Entrez.esearch(db="gene", term=gene.strip("\n")+"[sym]")
        gene_record = Entrez.read(gene_handle)
        gene_id_list = gene_record['IdList']

        # any results?
        if(gene_id_list):

            # go through each ID and get linked genome and genomic region
            for gene_id in gene_id_list:
                summary_handle = Entrez.esummary(db="gene", id=gene_id, report="full")
                summary_record = Entrez.read(summary_handle)['DocumentSummarySet']['DocumentSummary'][0]
                genomic_info = summary_record['GenomicInfo'][0]
                gene_version = summary_record['Status']
                genome_accession = genomic_info['ChrAccVer']
                chr_start = int(genomic_info['ChrStart'])
                chr_stop = int(genomic_info['ChrStop'])
                if(gene_version == "0"):
                    fasta_fh.write(">" + gene.strip("\n") + "@" + genome_accession + ":"
                                   + str(chr_start) + ":" + str(chr_stop) + "\n")
                    
                    # get actual sequence from the genomic region of interest
                    nt_handle = Entrez.efetch(db="nucleotide",
                                              id=genome_accession,
                                              rettype="fasta",
                                              strand=1,
                                              seq_start=chr_start+1,
                                              seq_stop=chr_stop+1)
                    nt_record = SeqIO.read(nt_handle, "fasta")
                    nt_handle.close()
                    fasta_fh.write("\n".join(wrap(str(nt_record.seq), 80)) + "\n")
                else:
                    genes_not_found_fh.write(gene.strip("\n") + ":old_version\n")
                print(nt_record.id)

        # empty list (based on gene label, no results could be found, literature)
        else:
            genes_not_found_fh.write(gene.strip("\n"))

gene_fh.close()
genes_not_found_fh.close()
fasta_fh.close()
