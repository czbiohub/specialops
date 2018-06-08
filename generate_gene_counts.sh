#!/bin/bash

for i in `ls *.tab`; do cut -f2 $i > $i.o; done;
paste `ls *.o` > all_counts.tsv
cut -f1 `ls *.tab | head -1` > genenames.txt
paste genenames.txt all_counts.tsv > gene_counts.tsv
ls *.tab > filenames.txt
tr "\n" "\t" < filenames.txt > filenames2.txt
cat <(echo -ne '\t') filenames2.txt > filenames.txt # add tab to beginning of filenames file to columns line up
#cat filenames.txt `echo "\n"` gene_counts.tsv > gene_counts_final.tsv
awk '{print}' filenames.txt gene_counts.tsv > gene_counts_final.tsv


rm *.o
rm genenames.txt
rm gene_counts.tsv 
rm all_counts.tsv
rm filenames2.txt
rm filenames.txt
