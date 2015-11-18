import sys
import os
from subprocess import call
#Obtain readset name, core genome sequence name and index name from the command line.
argu = sys.argv[1]
core_genome = sys.argv[2]
index_name = sys.argv[3]
fname = argu.split(".")
file_name=fname[0]
#This step aligns the given reads onto the index created from the core genomes previously. An alignment file containing the details of the different alignments of the reads to the different parts of the index is created as the output.
#Execute Bowtie2 alignment. Provide the readset name and index name as the input parameters and the name of the alignment file as the output parameter.
#In this case, the output file name is the same as the name of the input read file.
cmd="bowtie2 "+index_name+" "+file_name+".fastq -S "+file_name+".sam -a"
call(cmd,shell=True)
#Estimate abundances using the alignment file and the original sequence used for generating the Bowtie index as the input. 
#Apply Bitseq on Bowtie2 Output.
#In this case, the output file name is the same as the name of the input read file.
cmd="parseAlignment "+file_name+".sam -o "+file_name+".prob --trSeqFile "+core_genome+" --trInfoFile "+file_name+".tr --uniform --verbose  "
call(cmd,shell=True)
cmd="estimateVBExpression "+file_name+".prob -o "+file_name+" --outType RPKM  -t "+file_name+".tr"
call(cmd,shell=True)
#The final output consists of a Transcript file, a prob file and an abundance file, all with the same name as the input read file.
