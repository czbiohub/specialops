
#!/usr/bin/env python
# coding: utf-8

# import needed libraries
import pandas as pd
import sys
import os
import glob

#read in all files with the extension given
fileextension = sys.argv[1]
files = glob.glob(''.join(['*', fileextension]))


# initialize data frame
bowtiedf = pd.DataFrame(columns = ['File', 'TotalReads', 'OverallAlignmentPercent'],index = range(0,len(files)))

# read bowtie2 output and place into data frame
index = 0
for txtfile in files:
    df=pd.read_csv("%s" %txtfile,delimiter='\n',encoding='utf-8', engine ='python', header=None)
    rows_to_drop=range(1,14)
    df=df.drop(df.index[rows_to_drop])
    df=df.reset_index(drop=True)
    df = df[0].str.split(' ',expand=True)
    df = df[[0]]
    bowtiedf['File'][index] = txtfile
    bowtiedf['TotalReads'][index] = df[0][0]
    bowtiedf['OverallAlignmentPercent'][index] = df[0][1]
    index += 1


# write to CSV
bowtiedf.to_csv("Bowtie2output.csv")
