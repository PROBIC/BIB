from __future__ import print_function
import sys
import os
from subprocess import call
#Obtain readset name, core genome sequence name and index name from the command line.
if len(sys.argv) < 5:
    print("Usage: python %s [reads] core_genome_reference.fasta core_genome_index output" % sys.argv[0])
    print("""  where [reads] can be:
    "-1 reads_1.fastq -2 reads_2.fastq" (for paired end reads)
    "-U reads.fastq" (for unpaired reads)""")
    sys.exit(1)

read_file = sys.argv[1]
core_genome = sys.argv[2]
index_name = sys.argv[3]
filestem = sys.argv[4]
samfile = filestem + ".sam"
probfile = filestem + ".prob"
trfile = filestem + ".tr"
#This step aligns the given reads onto the index created from the core genomes previously. An alignment file containing the details of the different alignments of the reads to the different parts of the index is created as the output.
#Execute Bowtie2 alignment. Provide the readset name and index name as the input parameters and the name of the alignment file as the output parameter.
#In this case, the output file name is the same as the name of the input read file.
cmd="bowtie2 -a -x "+index_name+" "+read_file+" -S "+samfile
print(cmd)
call(cmd,shell=True)
#Estimate abundances using the alignment file and the original sequence used for generating the Bowtie index as the input. 
#Apply Bitseq on Bowtie2 Output.
#In this case, the output file name is the same as the name of the input read file.
cmd="parseAlignment "+samfile+" -o "+probfile+" --trSeqFile "+core_genome+" --trInfoFile "+trfile+" --uniform --verbose"
print(cmd)
call(cmd,shell=True)
cmd="estimateVBExpression "+probfile+" -o "+filestem+" -t "+trfile
print(cmd)
call(cmd,shell=True)
#The final output consists of a Transcript file, a prob file and an abundance file, all with the same name as the input read file.
