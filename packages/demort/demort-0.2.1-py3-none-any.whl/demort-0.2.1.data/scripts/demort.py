#!python
#===============================================================================
#INFORMATION
#===============================================================================
# Codes for DEMORT, a DEmultiplexing MOnitoring Report Tool. 
# 
# CEFE - EPHE - SEACONNECT 2019
# Guerin Pierre-Edouard
#
# DEMORT evaluates demultiplexed fastq files by computing various metrics.
# DEMORT is a python3 program.
#
# git repository : https://github.com/Grelot/demort
#
#==============================================================================
#NOTICE
#==============================================================================
#
#concept:
#=======
#DEMORT counts the number of reads for each fastq files for each folder
#It returns the results into a CSV file
#and gives a boxplot of the distribution of number of reads by fastq files
#for each folder into a PDF files
#input:
#=======
#IN_FOLDER: a file or a string containing a list of folders 
#containing fastq files to process
#case input folder file : each line is a path of a folder
#case input folder string : a list of path of folder separated by a coma ","
#NUM_THREADS: number of available cores in order to run in parrallel
#output:
#=======
#OUT_CSV_FILE: path of the file where to write a CSV file
#CSV's header="folder,fastqfile's name, number of reads"
#OUT_PDF_FILE: path of the file where to write a PDF file
#boxplot of the number of reads by files by folder
#usage:
#=======
#python3 src/demort.py -d IN_FOLDER -t NUM_THREADS -o OUT_CSV_FILE -p OUT_PDF_FILE
#IN_FOLDER can be 
#example:
#=======
#python3 src/demort.py -d tiny_demu,little_demu -t 8 -o mmm.csv -p mmm.pdf
#
#
#==============================================================================
#MODULES
#==============================================================================
import argparse
import os.path
import numpy
import matplotlib.pyplot as plt
import gzip
import csv
import Bio.SeqIO
from joblib import Parallel, delayed
import multiprocessing
#from Bio import SeqIO
#from Bio.Alphabet import IUPAC
#from Bio.Seq import Seq
#from Bio.SeqRecord import SeqRecord


#==============================================================================
#CLASS
#==============================================================================
class Fastqf:
    def __init__(self,fpath):
        self.fpath = fpath
        self.name= os.path.basename(fpath).split(".")[0]
        self.extension = os.path.basename(fpath).split(".")[1:]
        self.num_reads=0

class Folderf:
    def __init__(self,fpath,fqfiles):
        self.fpath = fpath
        self.name= os.path.basename(fpath)
        self.fqfiles=fqfiles


#==============================================================================
#FUNCTIONS
#==============================================================================
def process_arg_folder(arg_folder):
    """process argument in_folder
    return a list of folder paths
    """
    if os.path.isfile(arg_folder):
        with open(arg_folder) as f:
            list_folders = f.read().splitlines()
        f.close()
    else:
        list_folders = arg_folder.split(",")
    return(list_folders)

def list_fastq_folder(folder_path):
    """List all .fastq files in a specified directory + subdirectories.
    input argument is a folder path
    output is a list of Fastqf objects
    """
    fqfiles = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(folder_path):
        for file in f:
            if ('.fq.gz' or 'fastq.gz') in file:
                fqfile=Fastqf(os.path.join(r, file))
                fqfiles.append(fqfile)
    folderf=Folderf(folder_path,fqfiles)
    return(folderf)

def process_fastq(fastqf):
    """Count number of reads in a fastq files
    input argument is a Fastqf object
    output is an integer count_reads
    """
    if "gz" in fastqf.extension:
        handle_in = gzip.open(fastqf.fpath, "rt")
    else:
        handle_in=fastqf.fpath
    count_reads=0
    for read in Bio.SeqIO.parse(handle_in, "fastq"):
        count_reads+=1
    fastqf.num_reads=count_reads
    return(fastqf)


#==============================================================================
#ARGUMENTS
#==============================================================================
parser = argparse.ArgumentParser(description='DEMORT - DEmultiplexing MOnitoring Report Tool')
parser.add_argument("-p","--output_pdf", type=str)
parser.add_argument("-o","--output_csv", type=str)
parser.add_argument("-d","--inputFolder",type=str)
parser.add_argument("-t","--threads",type=int)


#==============================================================================
#MAIN
#==============================================================================
## record arguments
args = parser.parse_args()
out_pdf = args.output_pdf
out_csv = args.output_csv
in_folder = args.inputFolder
num_threads = args.threads

## list of folders to process
list_folders = process_arg_folder(in_folder)
print(list_folders)

## list of fastq files and number of reads by fastq file by folder
results={}
for f in list_folders:
    fqfolder = list_fastq_folder(f)
    results[fqfolder.name]=Parallel(n_jobs=num_threads)(delayed(process_fastq)(ff) for ff in fqfolder.fqfiles)

## write table
csv_file = open(out_csv, 'w')
with csv_file:
    writer=csv.writer(csv_file)
    for k in results.keys():
        for fq in results[k]:            
            writer.writerow([k, fq.name, fq.num_reads])

## write pdf
boxplot_data = []
for k in results.keys():
    k_boxplot_data =[]
    for fq in results[k]:
        k_boxplot_data.append(fq.num_reads)
    boxplot_data.append(k_boxplot_data)
plt.boxplot(boxplot_data,patch_artist=True,labels=[*results])
plt.savefig(out_pdf)


#==============================================================================