import os
import json
import pprint

from Bio import Entrez
from Bio import SeqIO

Entrez.email = "clo@kuleuven.be"
fasta = "genes_nt.fasta"
gene_list = os.path.join("data", "genes.txt")

with open(gene_list, "r") as f:
    for gene in f:
        print(gene)
        gene_handle = Entrez.esearch(db="gene", term=gene)
        gene_record = Entrez.read(gene_handle)
        gene_id_list = gene_record['IdList']
        if(gene_id_list):
            for gene_id in gene_id_list:
                summary_handle = Entrez.esummary(db="gene", id=5184378, report="full")
                summary_record = Entrez.read(summary_handle)['DocumentSummarySet']['DocumentSummary'][0]
                genomic_info = summary['GenomicInfo'][0]
                genome_accession = genomic_info['ChrAccVer']
                chr_start = genomic_info['ChrStart']
                chr_stop = genomic_info['ChrStop']
                print(genome_accession + " " + chr_start + " " + chr_stop)
                nt_handle = Entrez.efetch(db="nucleotide",
                                          id=genome_accession,
                                          rettype="fasta",
                                          strand=1,
                                          seq_start=chr_start,
                                          seq_stop=chr_stop)
                nt_record = SeqIO.read(nt_handle, "fasta")
                handle_nt.close()
                break
        else:
            print("nothing here")
        
        break
