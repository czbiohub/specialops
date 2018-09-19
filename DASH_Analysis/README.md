# DASH analysis
A wrapper script for subsampling, filtering, cutting TruSeq adaptors and running DASHit score guides on a directory of fastq.gz files. Recommend to run in tmux or screen.

### Installation
Transfer or copy the DASHwrapper.sh and the Python scripts (DASH_csv_format_interactive.py and DASH_csv_format.py) into the directory with the files you wish to perform the analysis on.

### Running the script

Use bash to run the script and follow with 3 arguments
1. the AWS path to your files
2. the path to the DASH guide library you want use to score your files
3. the name of your output file


```
bash DASHwrapper.sh s3://czbiohub-seqbot/fastqs/180907_A00111_0206_BH7W5WDSXX/rawdata/Amy_Lyden_AIH /mnt/data/nribo2_150_V2.csv AIH_Plate_02_1xPCR_DASHed
```

### Your output file

Your CSV output file will contain five columns
1. Guide library
2. Your filename
3. Total Reads DASHed (hit by scoreguides)
4. Total Reads in sample
5. Percent DASHed
