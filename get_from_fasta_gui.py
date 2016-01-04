# -*- coding: utf-8 -*-
#! /usr/bin/env python

"""
Created on Sat Jan 26 08:56:19 2013

@author: ido
"""


from Bio import SeqIO
import csv
import easygui as eg
import ntpath
#import regex as re
import re
import os

# import re


# Prepare lists
Items_list=[]
Items_input = []
No_item = []
path_cwd=os.getcwd()


# Check if input is number function
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def index_fasta(fasta_file):
    filePrefix='indexed_'
    fasta_filename=str(path_leaf(fasta_file))
##    if fasta_filename.split('_')[0]==filePrefix[:-1]:
##        fasta_filename=fasta_filename[len(filePrefix):]
##        existFile=True
##        print "new filename:", fasta_filename
    reIndex=False
    fas_input_path=ntpath.split(fasta_file)[0]
    if os.path.isfile(os.path.join(fas_input_path,(filePrefix+fasta_filename))):
        existFile=True
        indexYN=eg.boolbox(msg='''%s file was already prepared for indexing, do you wish to rewrite the file?
        This might take a couple of minutes...''' % fasta_filename, title='File already indexed', choices=('Yes', 'No'))
        if indexYN:
            reIndex=True
        else:
            index_file=os.path.join(fas_input_path, (filePrefix+fasta_filename))
            reIndex=False
    else:
##        reIndex=True
        existFile=False
    if reIndex or not existFile:
        print 'Preparing file %s for indexing' % fasta_filename
        index_file=os.path.join(fas_input_path, filePrefix+fasta_filename)
        indexOutputHandler=open(index_file, 'w')
        myRe=r"(^>[^\r\s])+"
        mySub=r"\1"
        with open(fasta_file, "rU") as fileread:
            for line in fileread:

                Result=re.search(myRe,line)
                if Result:
                    #print Result.groups()
                    new_line=re.sub(myRe, mySub, line)
                else:
                    new_line=line
                #print new_line
                indexOutputHandler.write(new_line)
        indexOutputHandler.close()
    print 'Indexing file, please wait...'
    unigene_dict = SeqIO.index(index_file, "fasta")
##    for i,key in enumerate(unigene_dict.keys()):
##        if i<10:
##            print "Dict key:", key, "Dict Value:", unigene_dict[key]
##        else:
##            break
    return unigene_dict


# Prompt for manual input
User_input='csv'
#eg.enterbox(msg='''
#Enter gene name (full or partial) or keword, or Unigene or ID number, seperated by commas and press enter.
#Example: Receptor, GSDF, 14343, etc.
#If keywords are in CSV file, enter CSV.''', title='User Input')



# File input
if User_input.upper() == 'CSV':
    csv_input_file=eg.fileopenbox(msg='Please select csv input file', title='CSV input file', filetypes =["*.csv", "CSV files"], default="%s\\*.csv" % path_cwd)
    csv_input_path=ntpath.split(csv_input_file)[0]
    with open(csv_input_file, 'rb') as fileread:
        inputreader = csv.reader(fileread)
        for row in inputreader:
            Items_input.append(row[0])
    fileread.close()

# Use manual input data instead of file
else:
    Items_User_input = User_input.split(',')
    for z in Items_User_input:
        Items_input.append(z.strip())
    annotYN=eg.boolbox(msg='Do you want to search keyword in annotation file?', title='Search annotation? ', choices=('Yes', 'No'))
    if annotYN:
        annot_file=eg.fileopenbox(msg='Please select csv annotation file', title='CSV annotation file', filetypes =["*.csv", "CSV files"], default="%s\\*.csv" % path_cwd)

# prepare fasta reference file
unigene_file=eg.fileopenbox(msg='Please select fasta reference file', title='FASTA ref file', filetypes =["*.fas", "*.fa", "*.fasta", "*.pep", "*.txt", "FASTA files"], default="%s/*.fas" % path_cwd)
Fasta_output=eg.filesavebox(msg='Save fasta output file as', title='Output fasta file', default="%s/output.fas" % path_cwd, filetypes =["*.fas", "*.fa", "*.fasta", "*.pep", "*.txt", "FASTA files"])
fasta_dict=index_fasta(unigene_file)
print len(fasta_dict)

#
# Headers for output table


# Go through all entries in Item_list
found_list=[]
row_count=0
IdRe=r"(^>[^\r\s]+)"
IdSub=r"\1"
if len(Items_input) > 0:
    fasta_seq=[]
    with open(Fasta_output,"w") as f:
        seq_counter=0
        for ID in Items_input:
            reID=re.sub(IdRe, IdSub, ID)
            Items_list=[]
            try:
                seqRecord=fasta_dict[reID]
                seq_counter+=1
                progress_percent=(float(seq_counter)/float(len(Items_input)))*100
                print 'Processing sequences from %s file, overall progress: %d%%' % (path_leaf(unigene_file),progress_percent)
                fasta_seq.append(seqRecord)

            except KeyError, IndexError:
                print "Cannot find %s in the reference file" % ID
                print "reID:", reID
##                for seq_record in SeqIO.parse(contig_file, "fasta"):
##                    if seq_record.id==row[0]:
##                        print 'Processing sequence %s from Contig file, overall progress: %d%%' % (seq_record.id,progress_percent)
##                        fasta_seq.append(seq_record)

    SeqIO.write(fasta_seq,Fasta_output,'fasta')

else:
#   Print appologize for missing entries
    print 'Sorry, list did not contain any items'
print 'Operation Completed!'




# That's all folks!