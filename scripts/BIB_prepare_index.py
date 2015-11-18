import sys
import os
from subprocess import call
#This step constructs the reference index to which the reads are eventually aligned. The input for this script are the core genomes while the output is a Bowtie index called core_genome_index.
cmd ="bowtie2-build core_genomes.fasta core_genome_index"
call(cmd,shell=True)
