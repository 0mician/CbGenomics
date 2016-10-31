#!/bin/bash

readonly SOFTWARE_REQUIRED=(fastq-dump spades.py ht-trim ht-filter)
readonly SRA_ACCESSION="SraAccList.txt"
readonly ARG="$1"
readonly SRA_FOLDER="sra"

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
	#echo "$line"
	fastq-dump -v --split-files --outdir $SRA_FOLDER $line
    done < "$SRA_ACCESSION"
}

# performs the QC of the reads
qc_fastq() {
    echo "todo"
}

# denovo assembly with spades
assembly(){
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
	*)
	    usage ; exit ;;
    esac
}
main
