#!/bin/bash

STRAINS_DIR=/mnt/data/CbGenomics/GeneSearch/FAA
PROTEINS_FILE=/mnt/data/CbGenomics/GeneSearch/proteins.faa

cd ${STRAINS_DIR}
# this loop will generate csv blast reports for each strains
for dir in */;
do
	echo "Processing $(basename $dir).faa"
	blastp -evalue 0.001 -query ${PROTEINS_FILE} -db $(basename ${dir}).faa -out ${dir}blast_report.txt -outfmt "6 qacc sacc qlen pident ppos nident mismatch positive evalue"
done

# this loop will regroup all the results in multiple csv files for different similarity levels
# filtering hits for 90-100% sequence identity
for dir in */;
do
    echo $(basename $dir) >> blast_results_90.csv
    echo $(basename $dir) >> blast_results_80.csv
    echo $(basename $dir) >> blast_results_70.csv
    echo $(basename $dir) >> blast_results_60.csv
    echo $(basename $dir) >> blast_results_50.csv
    
    cd $dir
    cat blast_report.txt | awk '{if($5 > 90) print $1","$2","$5}' >> ../blast_results_90.csv
    cat blast_report.txt | awk '{if($5 > 80) print $1","$2","$5}' >> ../blast_results_80.csv
    cat blast_report.txt | awk '{if($5 > 70) print $1","$2","$5}' >> ../blast_results_70.csv
    cat blast_report.txt | awk '{if($5 > 60) print $1","$2","$5}' >> ../blast_results_60.csv
    cat blast_report.txt | awk '{if($5 > 50) print $1","$2","$5}' >> ../blast_results_50.csv
    cd ../
done
