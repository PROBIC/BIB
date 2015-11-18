#!/bin/bash          
#These steps have to be performed at least once before running the pipeline. They include the extraction of the core genomes from the genome-set and the construction of the reference Bowtie index.
#Extraction of Core Genomes (Assuming that the necessary programs and scripts are available). The input can be modified as necessary. Multiple genomes may be included for the reference.
progressiveMauve --output=reference_set.xmfa reference_genomes.fasta
stripSubsetLCBs reference_set.xmfa reference_set.xmfa.bbcols core_reference_set.xmfa 500 4
perl xmfa2fasta.pl core_reference_set.xmfa
sed 's/-//g' core_reference_set.fasta > core_reference_set_gapless.fasta
#Construction of Bowtie index. If the core genomes are already available, this step can directly be executed.
bowtie2-build core_reference_set_gapless.fasta core_genome_index
