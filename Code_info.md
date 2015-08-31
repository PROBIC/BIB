The tool used for obtaining the core genomes from the list of raw genomes is progressiveMauve. This can be downloaded [here](http://darlinglab.org/mauve/download.html)

In order to obtain the core alignment from our list of input genomes, the following four steps have to be applied.

Step 1: get the alignment using progressiveMauve, run
`progressiveMauve --output=full_alignment.xmfa genome1.gbk genome2.gbk genome3.gbk genome4.gbk

Step 2: extract LCBs shared by all genomes
`stripSubsetLCBs full_alignment.xmfa full_alignment.xmfa.bbcols core_alignment.xmfa 500 4

the first number "500" is the minimum length of the LCB; the second number "4" indicates the minimum number of genomes that share a LCB

Step 3: concatenate all the LCBs
`perl xmfa2fasta.pl core_alignment.xmfa

You will get "core_alignment.fasta" in the current directory.

Step 4 : Remove gaps from the core alignment
`sed 's/-//g' core_alignment.fasta > core_alignment_gapless.fasta

Once the core alignment has been obtained, it can be used to construct a reference index using Bowtie2. Bowtie2 is available [here](http://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.2.6/)
The command for building the index is:
`bowtie2-build core_alignment_gapless.fasta core_alignment_gapless

Here, the first parameter is the name of the sequence from which the index has to be constructed. The second parameter is the name of the index.

The read files can be aligned to the reference index once it has finished being constructed. The command for this is :
`bowtie2 core_alignment_gapless read_file.fastq -S alignment_file.sam -a 

The input files are the reference index and the read file while the output file is the list of alignments for every read to every genome.
The different parameters that can be included for this command are given [here](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#getting-started-with-bowtie-2-lambda-phage-example).

