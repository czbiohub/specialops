# Sample Sheet Generation
An R script for generating sample sheets for the CZB TruSeq 8-12bp Indices

### Installation
Transfer or copy the folder "TruSeq_8-12bp_Indices_Sample_Sheet" containing the R script, the MasterComboList and the i7-i5-REVCOMP files. This can be accomplished by cloning the specialops directory from github. This folder also contains an example sample sheet.

```
git clone https://github.com/czbiohub/specialops.git
```

### Fill in the example sample sheet and save it as a CSV

You must fill in the following three columns:
1. Dual_Plate_ID
2. Barcode_Well
3. Sample_ID

The Sample_ID will become your fastq filename.

The rest of the columns are metadata columns.

**Metadata Option 1**: If all of your samples have the same metadata, you can leave them all blank and enter in values in the script later. All metadata will be the same for all samples (ex: for study ID, all will say "VAP"; for BioSample_Description, all will say "blood", for host, all will say "human").

**Metadata Option 2**: Alternatively if you have mixed samples in a sequencing run, you can fill in all of the metadata columns with the desired information (ex: you can fill in half with the study ID "VAP" and half with the study ID "mBAL", then for host, fill in all with "human"). Any blanks in these columns will appear as blanks in your final sample sheet.



### Editing the script

Open the Rmd file in RStudio.

1. Set the working directory on Line 20 by changing the path
2. Change the sequencer on Line 26 to iseq, miseq, nextseq or novaseq
3. Change the filename on Line 31 to the name of your sample sheet CSV that you prepared
4. Pick Metadata Option 1 or 2 from above
  ..* If using **Metadata Option 1**, fill in the values for the metadata on lines 38-48. Empty strings can be used for blank fields. Either DELETE, COMMENT (*CMD+SHIFT+C*), or set eval = FALSE in chunk options for Metadata Option 2.
  ..* If using **Metadata Option 2**, do nothing.

### Running the script

Run all by typing *OPTION+CMD+R*, or by clicking *Run -> Run All* in the upper right of the document.

### Open your CSV

Your CSV will appear with the date + sequencer + CZB-TruSeq-Sample-Sheet + your original filename. It will be formatted like the CZ Biohub Sequencing Submission Sample Sheet and can be copied and pasted into the Google submission.
