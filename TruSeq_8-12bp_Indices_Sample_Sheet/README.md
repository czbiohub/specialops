# Sample Sheet Generation
An R script for generating sample sheets for the CZB TruSeq 8-12bp Indices

### Installation
Transfer or copy the folder `"TruSeq_8-12bp_Indices_Sample_Sheet"` containing the Rmd script, and the `"2018-11-02-TRUSEQ-8-12BP-INDEX-PRIMERS-PLATES-001-to-012-MasterIndexList-FULL.csv"` files. This can be accomplished by cloning the specialops directory from github. This folder also contains an example sample sheet `"CZB-12bp-Sample-Input-Test.csv"` for editing, plus an example output `"2019-02-05_novaseq_CZB-TruSeq-SampleSheet_CZB-12bp-Sample-Input-Test.csv"`.

```
git clone https://github.com/czbiohub/specialops.git
```

### Open and fill in the example sample sheet and save it as a CSV

You must fill in the following three columns:
1. Dual_Plate_ID
2. Barcode_Well
3. Sample_ID

The Dual_Plate_ID should be in the format Dual-XXX. The Barcode_Well should be A1, B12, etc, not A01. The Sample_ID will become your fastq filename.

The rest of the columns are metadata columns. You can fill in all of your metadata, or you may leave some cells blank. In the Rmd script, you will have the option to fill in values which will populate the empty cells for a given column. For example, if you leave the "Host" column blank, you can type "human" in the script and the whole column will say "human". Alternatively, if you fill in two cells in the "Host" column to say "mouse" and leave the rest blank, you can type "human" in the script and all cells in that column will say "human" except the two cells you filled in with "mouse."

### Editing the script

Open the `"sample_sheet_ID_8-12bp.Rmd"`file in RStudio.

1. Change the sequencer on Line 20 to iseq, miseq, nextseq or novaseq
2. Change the filename on Line 25 to the name of your sample sheet CSV that you prepared (this can include a path to the filename)
3. In Metadata Step 1 of 2, on Lines 31-40, fill in a constant value to populate blank cells. If you wish to leave blank cells blank, give the variable an empty string `""`.

### Running the script

Run all by typing *OPTION+CMD+R*, or by clicking *Run -> Run All* in the upper right of the document.

### Open your CSV

Your CSV will appear with the date + sequencer + CZB-TruSeq-Sample-Sheet + your original filename. It will be formatted like the CZ Biohub Sequencing Submission Sample Sheet and can be copied and pasted into the Google submission.
