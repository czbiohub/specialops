#!/usr/bin/env python
# coding: utf-8

# # Undetermined Script Goals
# 1. Read in Undetermined files
# 2. Pull out barcodes and put in dataframe
# 3. Create a tally of all barcodes
# 4. Compare to original barcode plate used in experiment to identify 'hopping'
# 5. Compare to all barcode plates to identify 'mislabelling'

# # Script Outline
# 1. Create a function which reads in an Undetermined file
# 2. Create a function which pulls out barcodes and returns a data frame
# 3. Create a function which tallies all barcodes from a data frame
# 4. Create a function which identifies hopping
# 5. Create a function which identifies mislabelling
# 6. Run all functions and print out hopping and mislabelling results

import pandas as pd
import sys
import os

# # Set your index length, sequencer, number of undetermined barcodes you wish to investigate, your index plates, and your Undetermined file
file = sys.argv[1]
index_length = int(sys.argv[2]);
sequencer = sys.argv[3];
number_undetermined_barcodes = int(sys.argv[4]);
index_plates = sys.argv[5].split(",")
index_csv = sys.argv[6]
master_index_list = pd.read_csv(index_csv)



#PULL ALL BARCODES FROM AN UNDETERMINED FASTQ AND RETURN DATAFRAME
def pull_barcodes(file, index_length):
    undetermined_list = []
    for i, line in enumerate(open(file, 'r')):
        if i%4==0:
            line_split=line.split(":")[-1].strip('\n').split('+')
            if len(line_split[0]) == index_length:
                undetermined_dict = {'i7_barcode':line_split[0],
                                     'i5_barcode':line_split[1]}
                undetermined_list.append(undetermined_dict)
            else:
                raise Exception('Index length given does not match index length in Undetermined file')
    undetermined_df = pd.DataFrame(undetermined_list, index = None)
    return(undetermined_df)

#FIND THE TOP UNDETERMINED BARCODES FROM A DATAFRAME FROM pull_barcodes() AND RETURN DATAFRAME
def top_undetermined_barcodes(undetermined_barcodes_df, num_top_barcodes):
    tally = pd.DataFrame(undetermined_barcodes_df.groupby(['i7_barcode','i5_barcode']).size()).sort_values(by = 0, ascending = False)
    tally_subset = tally[0:num_top_barcodes].reset_index()
    tally_subset = tally_subset.assign(rank = tally_subset.index+1)
    tally_subset.columns = ['i7_barcode','i5_barcode','reads', 'rank']
    return tally_subset

def check_barcode_length(top_undetermined, index_length):
    if ((len(top_undetermined.loc[0]['i7_barcode']) and len(top_undetermined.loc[0]['i7_barcode'])) != index_length):
        raise Exception("Index length does not match Undetermined barcode length.")

#FILTER OUT ANY UNDETERMINED THAT HAVE GGGGGGGGGGG IN THEM AND RETURN pull_barcodes()/top_undetermined_barcodes() DATAFRAME
def filter_G_homopolymer_barcodes(top_undetermined):
    filtered = top_undetermined[(top_undetermined['i7_barcode']!='GGGGGGGGGGGG')
                                & (top_undetermined['i5_barcode']!='GGGGGGGGGGGG')
                                & (top_undetermined['i7_barcode'] !='GGGGGGGG') & (top_undetermined['i5_barcode'] !='GGGGGGGG')].reset_index()
    print(''.join(['Of ',str(len(top_undetermined)),' barcodes given, ', str(len(filtered)),' barcodes did not contain a G homopolymer.']))
    return filtered


def get_column_names(sequencer, index_length):
    if sequencer in ['iSeq','NextSeq','iseq','nextseq']:
        if index_length == 12:
            return 'i7_index_RC','i5_index_RC'
        elif index_length == 8:
            return 'i7_8bp_RC','i5_8bp_RC'
    elif sequencer in ['MiSeq','NovaSeq','miseq','novaseq']:
        if index_length == 12:
            return 'i7_index_RC','i5_index_F'
        elif index_lengh == 8:
            return 'i7_8bp_RC','i5_8bp_F'
    raise Exception("Not a valid combination of sequencer and index length")


#assert get_column_names('iseq',8) == ('i7_8bp_RC', 'i5_8bp_RC')

#IDENTIFY ANY BARCODES WHICH ARE TRUSEQ DUAL UNIQUE FROM top_undetermined_barcodes() DATAFRAME AND RETURN DATAFRAME WITH CONCLUSION
def TruSeq_dual_unique_check(top_undetermined,sequencer,index_length):
    check_barcode_length(top_undetermined, index_length)
    i7_name, i5_name = get_column_names(sequencer, index_length)
    ##
    outside_sample_sheet = [];
    for i in top_undetermined.index:
        outside_matches = master_index_list.loc[(master_index_list[i7_name]==top_undetermined.loc[i]['i7_barcode'])
              & (master_index_list[i5_name]==top_undetermined.loc[i]['i5_barcode'])]
        outside_dict = {'i7_barcode' : top_undetermined.loc[i]['i7_barcode'],
                            'i5_barcode' : top_undetermined.loc[i]['i5_barcode'],
                            'reads' : top_undetermined.loc[i]['reads'],
                       'rank' : top_undetermined.loc[i]['rank']}
        if outside_matches.empty:
            outside_dict.update( {'Dual_Plate_ID' : 'NA',
                            'well' : 'NA',
                            'demux_conclusion': "not a TruSeq dual-unique index pair"})
        else:
            outside_dict.update({
                            'Dual_Plate_ID' : outside_matches['Dual_Plate_ID'].values[0],
                            'well' : outside_matches['Barcode_Well'].values[0],
                            'demux_conclusion': "is a TruSeq dual-unique pair, may be outside sample sheet"})
        outside_sample_sheet.append(outside_dict)
    return pd.DataFrame(outside_sample_sheet, columns = ['i7_barcode','i5_barcode','reads','rank','demux_conclusion','Dual_Plate_ID','well'])


def TruSeq_dual_unique_filter(top_undetermined,sequencer,index_length):
    df = TruSeq_dual_unique_check(top_undetermined, sequencer, index_length)
    df = df[df['Dual_Plate_ID'] == 'NA']
    print(''.join(['Of ',str(len(top_undetermined)),' barcodes given, ', str(len(df)),' barcodes were not TruSeq dual-unique indices.']))
    return df[['i7_barcode','i5_barcode','reads','rank']].reset_index()[['i7_barcode','i5_barcode','reads','rank']]

# assert (
#     _TruSeq_dual_unique_filter(G_filtered,sequencer,index_length).values ==
#     _TruSeq_dual_unique_filter2(G_filtered,sequencer,index_length).values
# ).all()


#IDENTIFY ANY TOP UNDETERMINED BARCODES FROM top_undetermined_barcodes() DATAFRAME WHICH MAY HAVE HOPPED ON THIS RUN AND RETURN DATAFRAME
def hopped_indices(top_undetermined, dual_index_plates, sequencer, index_length):
    #check index len = undetermined length
    check_barcode_length(top_undetermined, index_length)

    #get column names
    i7_name, i5_name = get_column_names(sequencer, index_length)

    #read in master list of barcodes
    #master_index_list = pd.read_csv("../../TruSeq_8-12bp_Indices_Sample_Sheet/2018-11-02-TRUSEQ-8-12BP-INDEX-PRIMERS-PLATES-001-to-012-MasterIndexList-plus8bp_020619.csv")

    #subset to plates used in this run
    subset_master_index_list = master_index_list.loc[master_index_list['Dual_Plate_ID'].isin(dual_index_plates)]
    hopped_list = []
    hopped_indices = top_undetermined.loc[top_undetermined['i7_barcode'].isin(master_index_list[i7_name])
                                          & top_undetermined['i5_barcode'].isin (master_index_list[i5_name])]
    #identify the correct i5 based on a fixed i7 and print the correct plate and the location
    for i in hopped_indices.index:
        i7_barcode = hopped_indices.loc[i]['i7_barcode']
        i5_barcode = hopped_indices.loc[i]['i5_barcode']
        hopped_dict = {'i7_barcode':i7_barcode,
                      'i5_barcode': i5_barcode,
                      'reads':hopped_indices.loc[i]['reads'],
                      'rank':hopped_indices.loc[i]['rank']}

        filt_subset_master_index_list = subset_master_index_list[subset_master_index_list[i7_name]==i7_barcode]

        if filt_subset_master_index_list.empty: #if i7 barcode is not on your run
            hopped_dict.update({
               'i5_correct':'Not on a plate in your sample sheet',
               'dual_plate_id_i7_match': 'Not a plate in your sample sheet',
               'dual_plate_well_i7_match':'Not a plate in your sample sheet',
                'i5_correct_description': 'i7 barcode was not on a plate in your sample sheet, but matches a TruSeq i7 exactly'})
        elif (filt_subset_master_index_list[i5_name].values[0]) != (hopped_indices[hopped_indices['i7_barcode']==i7_barcode]['i5_barcode'].values[0]): #else if it is on the run & the i5 is not what it is supposed to be
            hopped_dict.update({
                           'i5_correct':filt_subset_master_index_list[i5_name].values[0],
                           'dual_plate_id_i7_match':filt_subset_master_index_list['Dual_Plate_ID'].values[0],
                           'dual_plate_well_i7_match':filt_subset_master_index_list['Barcode_Well'].values[0],
                'i5_correct_description': ''.join(['i7 barcode was on a plate in your sample sheet, but should match with the i5 listed in i5_correct. i7_barcode+i5_correct was plate ',filt_subset_master_index_list['Dual_Plate_ID'].values[0], ', barcode well ',filt_subset_master_index_list['Barcode_Well'].values[0]])})

        filt_subset_master_index_list = subset_master_index_list[subset_master_index_list[i5_name]==i5_barcode]

        if filt_subset_master_index_list.empty: # if i5 barcode is not on your run
            hopped_dict.update({
               'i7_correct':'Not on a plate in your sample sheet',
               'dual_plate_id_i5_match': 'Not a plate in your sample sheet',
               'dual_plate_well_i5_match':'Not a plate in your sample sheet',
            'i7_correct_description': 'i5 barcode was not on a plate in your sample sheet, but matches a TruSeq i5 exactly'})
        elif (filt_subset_master_index_list[i7_name].values[0]) != (hopped_indices[hopped_indices['i5_barcode']==i5_barcode]['i7_barcode'].values[0]):
            hopped_dict.update({
                           'i7_correct':filt_subset_master_index_list[i7_name].values[0],
                           'dual_plate_id_i5_match':filt_subset_master_index_list['Dual_Plate_ID'].values[0],
                           'dual_plate_well_i5_match':filt_subset_master_index_list['Barcode_Well'].values[0],
                            'i7_correct_description': ''.join(['i5 barcode was on a plate in your sample sheet, but should match with the i7 listed in i7_correct. i7_correct+i5_barcode was plate ',filt_subset_master_index_list['Dual_Plate_ID'].values[0], ', barcode well ',filt_subset_master_index_list['Barcode_Well'].values[0]])})
        hopped_list.append(hopped_dict)
    final_data = pd.DataFrame(hopped_list,columns = ['i7_barcode','i5_barcode','i7_correct','dual_plate_id_i5_match','dual_plate_well_i5_match','i7_correct_description','i5_correct','dual_plate_id_i7_match','dual_plate_well_i7_match','i5_correct_description','reads','rank'])

    if final_data.empty:
        print("No hopped indices within the plates on your sample sheet")
        return(final_data)
    else:
        print(''.join(['You have ', str(len(final_data)), ' hopped barcodes within the plate on your sample sheet']))
        return(final_data)



def filter_hopped_indices(filtered, hopped_index):
    leftover_indices = filtered
    if hopped_index.empty:
        leftover_indices = filtered
    else:
        for rank_num in list(filtered['rank']):
            if rank_num in list(hopped_index['rank']):
                leftover_indices = leftover_indices.loc[leftover_indices['rank'] != rank_num]

    print(''.join(['You have ',str(len(leftover_indices)),' barcodes remaining']))
    return leftover_indices.reset_index()[['i7_barcode','i5_barcode','reads','rank']]

def match_i5_or_i7(leftover_indices,sequencer,index_length,dual_index_plates):

    #check index len = undetermined length
    check_barcode_length(top_undetermined, index_length)

    #get column names
    i7_name, i5_name = get_column_names(sequencer, index_length)

    #read in master list of barcodes
    #master_index_list = pd.read_csv("../../TruSeq_8-12bp_Indices_Sample_Sheet/2018-11-02-TRUSEQ-8-12BP-INDEX-PRIMERS-PLATES-001-to-012-MasterIndexList-plus8bp_020619.csv")
    #subset to plates used in this run
    subset_master_index_list = master_index_list.loc[master_index_list['Dual_Plate_ID'].isin(dual_index_plates)]
    leftover_list = [];

    #match identical i7
    for i7_barcode in leftover_indices['i7_barcode']:
        filt_subset_master_index_list = subset_master_index_list[subset_master_index_list[i7_name]==i7_barcode]
        if filt_subset_master_index_list.empty:
            if i7_barcode in list(master_index_list[i7_name]):
                    leftover_dict = {'i7_barcode':i7_barcode,
                         'i5_barcode': leftover_indices[leftover_indices['i7_barcode']==i7_barcode]['i5_barcode'].values[0],
                         'reads': leftover_indices[leftover_indices['i7_barcode']==i7_barcode]['reads'].values[0],
                         'rank': leftover_indices[leftover_indices['i7_barcode']==i7_barcode]['rank'].values[0],
                         'i7_correct':i7_barcode,
                         'i5_correct':"i5 does not match an index in our TruSeq dataset",
                         'dual_plate_id':"Not a plate in your sample sheet",
                         'dual_plate_well':"N/A",
                         'description': 'i7 matches 100% with an i7 in TruSeq dataset, i5 does not'}
            else:
                continue
        else:
            leftover_dict = {'i7_barcode':i7_barcode,
                             'i5_barcode': leftover_indices[leftover_indices['i7_barcode']==i7_barcode]['i5_barcode'].values[0],
                             'reads': leftover_indices[leftover_indices['i7_barcode']==i7_barcode]['reads'].values[0],
                             'rank': leftover_indices[leftover_indices['i7_barcode']==i7_barcode]['rank'].values[0],
                             'i7_correct':i7_barcode,
                             'i5_correct':filt_subset_master_index_list[i5_name].values[0],
                             'dual_plate_id':filt_subset_master_index_list['Dual_Plate_ID'].values[0],
                             'dual_plate_well':filt_subset_master_index_list['Barcode_Well'].values[0],
                             'description': 'i7 matches 100% with an i7 in sample sheet, i5 does not'}
            leftover_dict['mismatches'] = sum(c1!=c2 for c1,c2 in zip(leftover_dict['i5_barcode'], leftover_dict['i5_correct']))
        leftover_list.append(leftover_dict)
    matchingi7 = len(leftover_list)
    print(''.join(['Of ',str(len(leftover_indices)),' barcodes given, ', str(matchingi7),' barcodes had an i7 perfectly matching an i7 in the plate on your sample sheet.']))

    #match identical i5
    for i5_barcode in leftover_indices['i5_barcode']:
        filt_subset_master_index_list = subset_master_index_list[subset_master_index_list[i5_name]==i5_barcode]
        if filt_subset_master_index_list.empty:
            if i5_barcode in list(master_index_list[i5_name]):
                    leftover_dict = {'i7_barcode':leftover_indices[leftover_indices['i5_barcode']==i5_barcode]['i7_barcode'].values[0],
                         'i5_barcode': i5_barcode,
                         'reads': leftover_indices[leftover_indices['i5_barcode']==i5_barcode]['reads'].values[0],
                         'rank': leftover_indices[leftover_indices['i5_barcode']==i5_barcode]['rank'].values[0],
                         'i7_correct':"i7 does not match an index in our TruSeq dataset",
                         'i5_correct': i5_barcode,
                         'dual_plate_id':"Not a plate in your sample sheet",
                         'dual_plate_well':"N/A",
                         'description': 'i5 matches 100% with an i5 in TruSeq dataset, i7 does not'}
            else:
                continue
        leftover_dict = {'i7_barcode': leftover_indices[leftover_indices['i5_barcode']==i5_barcode]['i7_barcode'].values[0],
                         'i5_barcode':i5_barcode,
                         'reads': leftover_indices[leftover_indices['i5_barcode']==i5_barcode]['reads'].values[0],
                         'rank': leftover_indices[leftover_indices['i5_barcode']==i5_barcode]['rank'].values[0],
                         'i7_correct':filt_subset_master_index_list[i7_name].values[0],
                         'i5_correct':i5_barcode,
                         'dual_plate_id':filt_subset_master_index_list['Dual_Plate_ID'].values[0],
                         'dual_plate_well':filt_subset_master_index_list['Barcode_Well'].values[0],
                         'description': 'i5 matches 100% with an i5 in sample sheet, i7 does not'}
        leftover_dict['mismatches'] = sum(c1!=c2 for c1,c2 in zip(leftover_dict['i7_barcode'], leftover_dict['i7_correct']))
        leftover_list.append(leftover_dict)
    print(''.join(['Of ',str(len(leftover_indices)),' barcodes given, ', str(len(leftover_list)-matchingi7),' barcodes had an i5 perfectly matching an i5 in the plate on your sample sheet.']))
    final_data = pd.DataFrame(leftover_list,columns = ['i7_barcode','i5_barcode','i7_correct','i5_correct','reads','rank','dual_plate_id','dual_plate_well','reads','mismatches','description'])

    return final_data




# # Run to pull out all the barcodes from the Undetermined fastq
undetermined_barcodes_df = pull_barcodes(file, index_length)


# # View your top undetermined barcodes
top_undetermined = top_undetermined_barcodes(undetermined_barcodes_df,number_undetermined_barcodes)
top_undetermined.to_csv("Top_Undetermined_Barcodes.csv")

# # Filter out any which are all "G" (adaptor reads)
G_filtered = filter_G_homopolymer_barcodes(top_undetermined)


# # View which barcodes were not TruSeq dual-unique index pairs and which were, but did not demux properly
# This may suggest samples had barcodes which were not listed on your sample sheet
TruSeqcheck = TruSeq_dual_unique_check(G_filtered,sequencer,index_length)
TruSeqcheck = TruSeqcheck[TruSeqcheck['demux_conclusion'] == "is a TruSeq dual-unique pair, may be outside sample sheet"]
TruSeqcheck.to_csv("TruSeq_Dual_Unique_Check.csv")

dualuniq_G_filtered = TruSeq_dual_unique_filter(G_filtered,sequencer,index_length)


# # View which barcodes had potential index hopping
# This suggest index hopping - does not include index hopping across plates not used on your library preparation run

hopped_index = hopped_indices(dualuniq_G_filtered,index_plates,sequencer, index_length)
hopped_index.to_csv("Hopped_Indices.csv")


# # Filter which barcodes which were not index hopping cases, or G homopolymers
# These may be samples which either had IDT synthesis errors or were frequently misread by the sequencer
leftover = filter_hopped_indices(dualuniq_G_filtered, hopped_index)

# # View which barcodes had a perfect match with an i7 or i5, but not with both
# These may be samples which either had IDT synthesis errors or were frequently misread by the sequencer
leftover_matched = match_i5_or_i7(leftover, sequencer, index_length,index_plates)
leftover_matched.to_csv("Leftover_Indices_Matched_to_i7_i5_SampleSheet.csv")
