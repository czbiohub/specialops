\* tool has undergone some testing


# Data Preprocessing

## Adapter Trimming

### [cutadapt](http://cutadapt.readthedocs.io/en/stable/guide.html#)\*
- input and output can be compressed, automatically detected based on file extension
- can run multithreaded: `-j`
- slower than AdapterRemoval
- can set minimum quality: `-q`

```bash
cutadapt -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTG -o R1_out.fastq.gz -p R2_out.fastq.gz R1.fastq.gz R2.fastq.gz -m 20 --trim-n -j 32
```

### [AdapterRemoval](https://github.com/MikkelSchubert/adapterremoval)\*
- input and output can be compressed: `--gzip`
- can detect adapters
- relatively fast
- can do quality trimming: `--trimqualities and --minquality`
- automatically discards reads that are less than `--minlength (default 15)`

```bash
AdapterRemoval --file1 R1.fq.gz --file2 R2.fq.gz --basename samplename
--output1 samplename.pair1.truncated.fq --output2 samplename.pair2.truncated.fq --adapter1 AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC --adapter2 AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTG --trimns --minlength 20 --threads 32
```

### [Trimmomatic](http://www.usadellab.org/cms/index.php?page=trimmomatic)
- input and output can be compressed
  - comes with FASTA file of adapters
  - can do quality trimming
  - many options

```bash
trimmomatic PE -phred33 input_forward.fq.gz input_reverse.fq.gz output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
```

### [trim-galore](https://github.com/FelixKrueger/TrimGalore)
- wrapper of fastqc and cutadapt

### [fastp](https://github.com/OpenGene/fastp)\*
See _Quality Filtering_

### [Porechop](https://github.com/rrwick/Porechop)\*
For adaptor trimming of Nanopore data
- checks data against database of Nanopore adaptors, then trims the ones that match best

## Quality Filtering
All the trimming tools can do simple trimming based on quality.

### [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)\*
For quality assessment of raw reads, not actual processing.

### [MultiQC](https://github.com/ewels/MultiQC)\*
Creates html report that aggregrates output reports from other tools like FastQC, fastp, Kraken, Bowtie2, etc.

### [illumina-utils](https://github.com/merenlab/illumina-utils)
Suite of tools for filtering Illumina Paired-End reads.

### [PRICE](http://derisilab.ucsf.edu/software/price/)

### [AfterQC](https://github.com/OpenGene/AfterQC)

### [fastp](https://github.com/OpenGene/fastp)\*
Successor to AfterQC. Faster with multithreading support.
- pipeline to quality filter, trim, read correction, etc
- supposed to be a comprehensive set of tools for sequencing data
- generates json and html
- automatically detects adaptor
- duplication rate
- very fast
  - testing on Alameda Klebsiella data

```bash
fastp -i 15AC0001938_ST258.fastq -o fastp_15AC0001938_ST258.fastq.gz -p --json fastp_15AC0001938_ST258.json --html fastp_15AC0001938_ST258.html -R 'fastp_15AC0001938_ST258.report'
Detecting adapter...
No adapter detected

Read1 before filtering:
total reads: 2724369
total bases: 403855082
Q20 bases: 395890604(98.0279%)
Q30 bases: 375929556(93.0853%)

Read1 after filtering:
total reads: 2723284
total bases: 403766569
Q20 bases: 395856949(98.041%)
Q30 bases: 375908913(93.1006%)

Filtering result:
reads passed filter: 2723284
reads failed due to low quality: 1085
reads failed due to too many N: 0
reads failed due to too short: 0
reads with adapter trimmed: 0
bases trimmed due to adapters: 0

Duplication rate (may be overestimated since this is SE data): 29.8877%

JSON report: fastp_15AC0001938_ST258.json
HTML report: fastp_15AC0001938_ST258.html

fastp -i 15AC0001938_ST258.fastq -o fastp_15AC0001938_ST258.fastq.gz -p --json fastp_15AC0001938_ST258.json --html fastp_15AC0001938_ST258.html -R fastp_15AC0001938_ST258.report
fastp v0.19.3, time used: 41 seconds
```
- for single-end data, cannot detect multiple adapters

# Read Mapping

### Minimap2\*
Read mapper for both short and long reads.
- local mapping
- best for long read mapping

### Bowtie2\*
Short-read mapper.

# Annotation

### Mugsy-Annotator
Uses whole-genome alignment to identify anomalies in annotated gene structures.

### Transposome
Annotate from read mapping.

### ISEScan

### Prokka\*
Fast annotation of assemblies and draft genomes based on homology.

## Visualization

### [Artemis](http://sanger-pathogens.github.io/Artemis/Artemis/)\*
Popular genome browser.

# Mobile Genetic Element Detection

## Plasmid Detection

### plasmidSPAdes\*
- based on read coverage (bias in sequencing for plasmids)

```
spades.py --plasmid ...
```

### Plasmid Finder
- detection based on homology to plasmid databases


## Genomic Island Detection

### IslandViewer4\*
 - union of different tools based on sequence composition and homology

### Alien Hunter

## Pan Genome Analysis

### Roary\*
- takes .gff files as input (recommends Prokka annotations in tutorial)
- looks at coding regions in annotated genomes
- separates core (intersection) and accessory (complement) genomes

### [Piggy](https://github.com/harry-thorpe/piggy)\*
- takes Roary output folder as input
- looks at intergenic regions to complement Roary

### PopPUNK\*
- k-mer based approach to calculate core and accessory genome distances

## Other Tools

### [pyfaidx](https://github.com/mdshw5/pyfaidx)\*
- facilitates complex manipulation of FASTA files with minimal programming knowledge


### jModelTest\*
Evaluates a multiple alignment and outputs best mutation rate model

```
java -jar jModelTest.jar -d /data/snippy_out/core.aln -g 4 -i -f -AIC -BIC -a
```

### TreeGubbins
Can identify clusters in phylogeny by calculating density of each node and comparing to mean expected density

### [Snippy](https://github.com/tseemann/snippy)\*
SNP-calling pipeline by same people that made prokka
- BWA-mem + samtools + freebayes
- one run per sample, can generate SNP alignment fasta if all against same reference using `snippy-core`
- fairly modular, run `snippy-core` on different snippy outputs to add or remove organisms
- decent versioning documentation, but need to install from github repo since conda installation is too old
