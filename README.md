# BIB
Bayesian Identification of Bacteria

The following tools are required for the pipeline :

1. [progressiveMauve](http://darlinglab.org/mauve/download.html) - For the extraction and alignment of the core genomes.
2. [Bowtie2](http://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.2.6/) - For the construction of the reference index and for the alignment of the reads.
3. [Bitseq](https://github.com/BitSeq/BitSeq) - For the estimation of the abundances from the alignment of the reads.


###Extraction of the core genomes

In order to obtain the core alignment from our list of input genomes, the following four steps have to be applied.

Step 1: get the alignment using progressiveMauve, run

``progressiveMauve --output=full_alignment.xmfa genome1.fasta genome2.fasta genome3.fasta genome4.fasta``

Step 2: extract LCBs shared by all genomes

``stripSubsetLCBs full_alignment.xmfa full_alignment.xmfa.bbcols core_alignment.xmfa 500 4``

the first number "500" is the minimum length of the LCB; the second number "4" indicates the minimum number of genomes that share a LCB

Step 3: concatenate all the LCBs

``perl xmfa2fasta.pl core_alignment.xmfa``

You will get "core_alignment.fasta" in the current directory.

Step 4 : Remove gaps from the core alignment

``sed 's/-//g' core_alignment.fasta > core_alignment_gapless.fasta``

Additional information about the parameters required for the execution of progressiveMauve is provided [here](http://darlinglab.org/mauve/user-guide/progressivemauve.html).

###Construction of the reference index
Once the core alignment has been obtained, it can be used to construct a reference index using Bowtie2.
The command for building the index is:

``bowtie2-build core_alignment_gapless.fasta core_alignment_gapless``

Here, the first parameter is the name of the sequence from which the index has to be constructed. The second parameter is the name of the index. 

###Alignment of the reads

The read files can be aligned to the reference index once it has finished being constructed. The command for this is :
``bowtie2 core_alignment_gapless read_file.fastq -S alignment_file.sam -a ``

The input files are the reference index and the read file while the output file is the list of alignments for every read to every genome. The different parameters that can be included for this command are given [here](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#the-bowtie2-aligner).

### Estimation of strains and their abundances

The abundance estimation process is performed through BitseqVB. Additional information on the usage of Bitseq is provided [here](http://bitseq.github.io/).

This process consists of two steps. The first step involves the computation of probabilities for every alignment.

``$BitSeq/parseAlignment  alignment_file.sam -o alignment_info.prob --trSeqFile core_alignment_gapless.fasta --trInfoFile genome_info.tr --uniform --verbose``

The alignment file produced in the previous step along with the gapless alignment of the core genomes is used as the input while the .prob file containing the probabilities of every alignment of each read and the .tr file containing the list of the genomes used to build the alignment file are produced as the outputs.

The second step estimates the relative transcript expression using a VB algorithm with the .prob file taken as the input.

``BitSeq/estimateVBExpression -o abundance alignment_info.prob -t genome_info.tr``

The sampler produces the file abundance.m_alphas which contains three columns. The first one corresponds to the estimated relative transcript expression levels (mean theta). The next two columns contain the parameters of the marginal Beta distribution describing the estimated distribution per transcript (alpha, beta). The resulting file will contains M lines, one for each transcript.

#Abundance estimation pipeline

The alignment of the reads to the reference index and the estimation of the abundances of the strains from this alignment can be executed in a single step for multiple experiments by running the provided pipeline scripts as follows :

``python pipeline_input.py``

The pipeline_input script in turn calls the pipeline script for all the read sets given within the script. Additional read sets can be added by including the following line in the script.

``python pipeline.py new_readset.fastq``

The pipeline script aligns the given reads to a pre-constructed reference index. This index can be specified as required on line 13 of the pipeline.py file. The alignment is then directly used by the script to estimate the abundances using Bitseq as specified above. The output files produced contain the predicted abundances of the strains. These files have the same name as the readset files given as the input in the pipeline_input script.



