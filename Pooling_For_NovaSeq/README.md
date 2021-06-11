# Pooling by MiSeq
The bash script for downloading MiSeq .gz files and creating a CSV with the total read counts and adaptor read counts for pooling

### Installation
Transfer or copy the MiSeqPooling.sh into the directory you wish to transfer your files (locally or on AWS). This can be accomplished by cloning the specialops directory from github.

```
git clone https://github.com/czbiohub/specialops.git
```

### Open a screen or terminal session

Open up a tmux or screen session, as the downloading, unzipping and grep can take up to a day if your files are large. For a standard MiSeq micro or nano, expect 30 mins - 2 hours.

### Running the script

Use bash to run the script and follow with 2 arguments
1. the path to your files
2. the desired name of your output CSV


```
bash MiSeqPooling.sh s3://czbiohub-seqbot/fastqs/180615_NB501961_0126_AHWV5YAFXX/rawdata OPS_006_MiSeq_TestCounts
```

Note: each sequencer has a unique identifier that begins each read, making the script different for MiSeq vs NextSeq vs iSeq etc. If pooling by NextSeq, please use the NextSeqPooling.sh script. When in doubt, check the first line of your fastq file and modify the script to reflect it if necessary. It is usually "@" followed by letters and numbers.

### Open up the CSV file

The CSV file will contain three columns
1. Your filename
2. The total read counts
3. The read counts to the adaptor

### Convert into pooling values

Subtract the number of adaptor read counts from the number of total read counts. Normalize your volumes to the sample with the lowest read counts.
