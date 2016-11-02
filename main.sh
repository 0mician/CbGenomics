#!/bin/bash

readonly SOFTWARE_REQUIRED=(fastq-dump spades.py ht-trim ht-filter fastqc)
readonly SRA_ACCESSION="SraAccList.txt"
readonly ARG="$1"
readonly SRA_FOLDER="/mnt/data/CbGenomics/"

# progress prompt
progress_prompt(){
    echo -e "\n######  $1 ######"
}

usage(){
    echo "Usage : $0 [retrieve_sra | qc_fastq | assembly | annotation ]"
}

# checks if a given software is available on the system (not testing for specific version)
is_installed() {
    local software=$1
    command -v $software >/dev/null 2>&1 || { return 1; }
    return 0
}

# checks if all software required are available
software_checklist() {
    progress_prompt "software checklist"
    for software in "${SOFTWARE_REQUIRED[@]}"
    do
	echo -n "Checking if ${software} is installed..........."
 	if is_installed "${software}"; then
	    echo "OK"
	else
	    echo "NOK, $software not installed or not in PATH - exiting"
	    exit -1
	fi
    done
}

# retrieves all the fastq files
retrieve_sra(){
    progress_prompt "retrieving SRA files"
    while IFS= read -r line; do
	fastq-dump -v --split-files --outdir $SRA_FOLDER/$line $line
    done < "$SRA_ACCESSION"
}

# performs the QC of the reads
qc_fastq() {
    while IFS= read -r line; do
	# Reports of pre-processing quality control of fastq files
	progress_prompt "pre-processing quality control"
	mkdir $SRA_FOLDER/$line/pre
	fastqc --outdir $SRA_FOLDER/$line/pre --extract --threads 4 \
	       $SRA_FOLDER/$line/${line}_1.fastq \
	       $SRA_FOLDER/$line/${line}_2.fastq

	# QC of the reads (Trimming)
	progress_prompt "Trimming"
	ht-trim -i $SRA_FOLDER/$line/${line}_1.fastq \
		-o $SRA_FOLDER/$line/${line}_1_trim.fastq
	ht-trim -i $SRA_FOLDER/$line/${line}_2.fastq \
		-o $SRA_FOLDER/$line/${line}_2_trim.fastq

	# QC of the reads (size exclusion)
	progress_prompt "Size exclusion"
	ht-filter --paired --filter length \
		  -i $SRA_FOLDER/$line/${line}_1_trim.fastq \
		     $SRA_FOLDER/$line/${line}_2_trim.fastq \
		  -o $SRA_FOLDER/$line/${line}_final.fastq

	# Reports of post-processing QC of the fastq files
	progress_prompt "post-processing quality control"
	mkdir $SRA_FOLDER/$line/post
	fastqc --outdir $SRA_FOLDER/$line/post --extract --threads 4 \
	       $SRA_FOLDER/$line/${line}_final_1.fastq \
	       $SRA_FOLDER/$line/${line}_final_2.fastq \
	       $SRA_FOLDER/$line/${line}_final_s.fastq

	# Clean up folder fastq files (unless you have 1Tb+ free space)
	rm $SRA_FOLDER/$line/${line}_1_trim.fastq \
	   $SRA_FOLDER/$line/${line}_2_trim.fastq \
	   $SRA_FOLDER/$line/${line}_1.fastq \
	   $SRA_FOLDER/$line/${line}_2.fastq
	
    done < "$SRA_ACCESSION"
}

# denovo assembly with spades
assembly(){
    while IFS= read -r line; do
	spades.py -t 8 -k 21,33,55,77 --careful \
		  --pe1-1 $SRA_FOLDER/$line/${line}_final_1.fastq \
		  --pe1-2 $SRA_FOLDER/$line/${line}_final_2.fastq \
		  --s1 $SRA_FOLDER/$line/${line}_final_s.fastq \
		  -o $SRA_FOLDER/$line/asm
    done < "$SRA_ACCESSION"
}

# Annotation with prokka
annotation(){
    echo "todo"
}

main() {
    if [ -z "$ARG" ]
    then
     	usage ; exit ;
    fi

    software_checklist

    case "$ARG" in
	"retrieve_sra")
	    retrieve_sra ;;
	"qc_fastq")
	    qc_fastq ;;
	"assembly")
	    assembly ;;
	"annotation")
	    annotation ;;
	*)
	    usage ; exit ;;
    esac
}
main
