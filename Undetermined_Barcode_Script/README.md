# Undetermined Barcode Script

This script will help you investigate any indexing barcodes read by an Illumina sequencer which got demuxed into the "Undetermined" fastq file. If a barcode pair was not on your sample sheet, but was read by the sequencer, it will appear in this file. Barcodes can appear in this file for a number of reasons:

1. PhiX barcode
2. Indexing read failed (no read is interpreted as darkest color and becomes G homopolymer or T homopolymer)
3. Index hopping (i7 from one sample crossed with i5 of another sample)
4. Wrong indices were put on sample sheet due to human error or barcode plate being incorrectly labelled (barcodes match another TruSeq dual unique pair)
5. Barcode misread by sequencer (common in small numbers, one or two bases mismatch with actual barcode on sample sheet)
6. Barcode synthesized incorrectly by IDT (rare, but possible)

## Before running script

Download your Undetermined file from your sequencing run and unzip it. Also, make sure you know the sequencer used, whether 12 or 8 bp sequences were read and which Dual-XXX plates were used.

## Running script

Run from a bash command line interface. Enter the following information in the correct order after the call to the script.

1. Path to Undetermined file
2. Index length
3. Sequencer
4. Number of Undetermined barcodes you would like to look at (varies for your purposes, but 100 is usually a good start)
5. Dual index plate ids (separated by a comma, no spaces)
6. Path to TruSeq index barcode file

**Example bash command**
```
python Processing_Undetermined_Script_V3.py ../Undetermined_S0_R1_001.fastq 12 iseq 100 Dual-025,Dual-026 ../TruSeq_8-12bp_Indices_Sample_Sheet/2018-11-02-TRUSEQ-8-12BP-INDEX-PRIMERS-PLATES-001-to-012-MasterIndexList-plus8bp_020619.csv
```
## CSV output reports

You will now find in the directory four CSV files which contain information about your Undetermined fastq. Files will be empty if no barcodes fit the category.

1. ```Top_Undetermined_Barcodes.csv``` This will contain the top N barcodes in your Undetermined file.
2. ```TruSeq_Dual_Unique_Check.csv``` This will contain any Undetermined barcodes which match a TruSeq dual unique pair not on your sample outside_sample_sheet. This will contain barcodes in Undetermined for reason ```4``` in the intro.
3. ```Hopped_Indices.csv``` This will contain any Undetermined barcodes with suspected index hopping among the plates on your samples sheet, with the plate and well id of the i7 and i5 which may have swapped. This will contain barcodes in Undetermined for reason ```3``` in the intro.
4. ```Leftover_Indices_Matched_to_i7_i5_SampleSheet.csv``` This will contain any Undetermined barcodes which had an i7 or i5 perfectly matching your TruSeq barcodes on your sample sheet, but which did not have the paired i7 or i5 which perfectly matched a TruSeq dual unique pair. This will contain barcodes in Undetermined for reason ```5 or 6``` in the intro.
