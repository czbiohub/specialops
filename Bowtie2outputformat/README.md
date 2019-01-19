### Format bowtie2 output from multiple log/txt files
This python script will format all files redirected from bowtie2 output to have the index, filename, total reads, and overall alignment rate into a CSV format

### Installation
Transfer or copy the Bowtie2_csv_format.py into the directory where your output files are located (locally or on AWS). This can be accomplished by cloning the specialops directory from github.

```
git clone https://github.com/czbiohub/specialops.git
```

### Running the script

Pass the extension to which all your bowtie2 output files end with to the python command from your command line

```
python Bowtie2_csv_format.py .log
```

### Open up the CSV file

Your output CSV will be "Bowtie2output.csv

The CSV file will contain four columns
1. The index of the file
2. The filename
3. The total reads
4. The overall alignment rate from Bowtie2
