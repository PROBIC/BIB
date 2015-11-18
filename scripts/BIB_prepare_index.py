import sys
import os
from subprocess import call
#This step constructs the reference index to which the reads are eventually aligned. 
#The input for this script are the core genomes while the output is a Bowtie2 reference index.
#The reference index produced is of the same name as the input core genomes.
argu = sys.argv[1]
core_index = sys.argv[2]
fname = argu.split(".")
core_genomes = fname[0]
cmd ="bowtie2-build "+core_genomes+".fasta "+core_index
call(cmd,shell=True)
