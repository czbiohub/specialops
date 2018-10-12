#$1 will be the file path to your aws bucket with the MiSeq reads (ex:s3://czbiohub-seqbot/fastqs/180612_M05295_0117_000000000-G1GKV/rawdata/)
aws s3 sync $1 . --exclude "*" --include "*.fastq.gz"

#search for the read counts
zgrep -c "@M0" *R1*.gz > readcounts.txt

#add the adaptor read counts
zgrep -c ^GATCGGAAGAGCACACGTCT *R1*.gz > adaptorcounts.txt

#cut the first column of adaptor counts
cut -d: -f2 < adaptorcounts.txt > adaptorcountsnumbers.txt

#convert : to ,
tr ":" "," < readcounts.txt > readcounts.csv

#add headers to your csv output, $2 will be the filename
printf "SampleFilename,TotalReadCounts,AdaptorReadCounts\n" > $2.csv

#add filenames/readcounts + adaptor read counts to csv output
paste -d , readcounts.csv adaptorcountsnumbers.txt >> $2.csv

#remove intermediate files
rm readcounts.txt
rm adaptorcounts.txt
rm adaptorcountsnumbers.txt
rm readcounts.csv
