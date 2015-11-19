from __future__ import print_function
import sys
import os
from subprocess import call
#This step constructs the reference index to which the reads are eventually aligned. 
#The input for this script are the core genomes while the output is a Bowtie2 reference index.
#The reference index produced is of the same name as the input core genomes.
if len(sys.argv) < 3:
    print("Usage: python %s core_genome_reference.fasta core_genome_index" % sys.argv[0])
    sys.exit(1)

core_genomes = sys.argv[1]
core_index = sys.argv[2]
cmd ="bowtie2-build "+core_genomes+" "+core_index
call(cmd,shell=True)
