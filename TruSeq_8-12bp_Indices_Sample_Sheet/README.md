# Sample Sheet Generation
An R script for generating sample sheets for the CZB TruSeq 8-12bp Indices. If you are creating a 384-well barcode plate from the 96-well barcode plates, note that the 384-well plate must be made according to the layout below.


### Installation
Transfer or copy the folder `"TruSeq_8-12bp_Indices_Sample_Sheet"`. This can be accomplished by cloning the specialops directory from github. 

```
git clone https://github.com/czbiohub/specialops.git
```

This folder contains:
+ an example input CSV `"CZB-Sample-Input-Test_96.csv"` intended for use on a 96-well plate
an example input CSV `"CZB-Sample-Input-Test_384.csv"` intended for use on a 384-well plate
+ an example output sample sheet CSV `"2019-02-05_novaseq_12bp_CZB-TruSeq-SampleSheet_CZB-Sample-Input-Test.csv"`
+ the master index list with the 8 and 12 bp sequences  `"2018-11-02-TRUSEQ-8-12BP-INDEX-PRIMERS-PLATES-001-to-012-MasterIndexList-plus8bp.csv"` 
+ the Rmd script to be run in RStudio `"sample_sheet_ID_8-12bp_96-384well.Rmd"`


### Open and fill in the example input CSV and save it as a new CSV

You must fill in the following three columns for the 96-well plate input sheet:
1. Dual_Plate_ID
2. Barcode_Well
3. Sample_ID

The Dual_Plate_ID should be in the format Dual-XXX. The Barcode_Well should be A1, B12, etc, not A01. The Barcode_Well corresponds to the well on the TruSeq barcode plate utilized for a particular sample. The Sample_ID will become your fastq filename.

You must fill in the following two columns for the 384-well plate input sheet:
1. Sample_Well
2. Sample_ID

The Sample_Well should be A1, B12, etc, not A01. The Sample_Well corresponds to the well location on your 384-well plate for a particular sample. The Sample_ID will become your fastq filename.

The rest of the columns are metadata columns. You can fill in all of your metadata, or you may leave some cells blank. In the Rmd script, you will have the option to fill in values which will populate the empty cells for a given column. For example, if you leave the "Host" column blank, you can type "human" in the script and the whole column will say "human". Alternatively, if you fill in two cells in the "Host" column to say "mouse" and leave the rest blank, you can type "human" in the script and all cells in that column will say "human" except the two cells you filled in with "mouse."

### Editing the script

Open the `"sample_sheet_ID_8-12bp_96-384well.Rmd"`file in RStudio.

1. Change the sequencer on Line 20 to iseq, miseq, nextseq or novaseq
2. Change the index length on Line 25 to either 8 or 12 depending on desired length
3. Change the filename on Line 30 to the name of your sample sheet CSV that you prepared (this can include a path to the filename)
4. OPTIONAL If using the 384-well input sheet, change the Plate_IDs on line 36 to match the plates by quadrant to make the 384-well plate.
5. In Metadata Step 1 of 2, on Lines 52-61, fill in a constant value to populate blank cells. If you wish to leave blank cells blank, give the variable an empty string `""`.

### Running the script

Run all by typing *OPTION+CMD+R*, or by clicking *Run -> Run All* in the upper right of the document.

### Open your CSV

Your CSV will appear with the date + sequencer + CZB-TruSeq-Sample-Sheet_384 + your original filename (if using a 384-well plate) or date + sequencer + CZB-TruSeq-Sample-Sheet_96 + your original filename  (if using a 96-well plate). It will be formatted like the CZ Biohub Sequencing Submission Sample Sheet and can be copied and pasted into the Google submission.
