import sys
import os
from subprocess import call
#Obtain file name from the command line
argu = sys.argv[1]
fname = argu.split(".")
file_name=fname[0]
#Align Reads on Bowtie2
#Change directory to where the read files are located
os.chdir("readset_location")
#Execute Bowtie2 alignment. Provide the readset name and index name as the input parameters and the name of the alignment file as the output parameter.
#In this case, the output file name is the same as the name of the input read file.
cmd="./bowtie2 Bowtie_index "+file_name+".fastq -S "+file_name+".sam -a"
call(cmd,shell=True)
#Apply Bitseq on Bowtie2 Output
#Estimate abundances using the alignment file and the original sequence used for generating the Bowtie index as the input. 
cmd="./parseAlignment "+file_name+".sam -o "+file_name+".prob --trSeqFile Input sequence.fasta --trInfoFile "+file_name+".tr --uniform --verbose  "
call(cmd,shell=True)
cmd="./estimateVBExpression "+file_name+".prob -o "+file_name+" --outType RPKM  -t "+file_name+".tr"
call(cmd,shell=True)
#The final output consists of a Transcript file, a prob file and an abundance file, all with the same name as the input read file.