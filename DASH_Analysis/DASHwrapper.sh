#! /bin/bash
# USAGE
# bash DASHwrapper.sh awspath path_to_DASHguides outputfile

aws_path=$1
path_to_DASHguides=$2
output_file=$3

#sync and unzip files
aws s3 sync $aws_path .
rm Undetermined*
gunzip *.gz

#subsample to 100,000 reads
for i in *.fastq.gz;
do seqtk sample -s100 $i 1000000 > sub1m_${i:0:-3};
done;

#filter files using PriceSeqFilter
for i in sub1m_*R1_001.fastq ; do PriceSeqFilter -a 20 -fp ${i:0:-11}1_001.fastq ${i:0:-11}2_001.fastq -op filt-85-98-90_${i:0:-11}1.fq filt-85-98-90_${i:0:-11}2.fq -pair both -rqf 85 0.98 -rnf 90; done;

#convert fastq to fasta
for i in filt*; do seqtk seq -A $i > ${i:0:-1}asta; done;

#cut TruSeq adaptors
pip install cutadapt
for i in filt*1.fasta; do cutadapt -j 16 -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT -o cut-${i:0:-7}1.fasta -p cut-${i:0:-7}2.fasta $i ${i:0:-7}2.fasta -m 36; done;

#run score_guides
for i in filt*cut*.fasta; do score_guides $path_to_DASHguides $i >> $output_file.txt; done

tr "=" "," < $output_file.txt  > $output_file.csv
printf "SampleFilename,PercentDASHable\n" > ${output_file}_unformatted.csv

#remove intermediate files
rm filt*cutNEBF.fasta
rm filt*cutNEBR.fasta
rm filt*.fq
rm filt*R1.fasta
rm filt*R2.fasta

#prepare to run python
pip install pandas
python DASH_csv_format_interactive.py $output_file
