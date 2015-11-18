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

##Abundance estimation pipeline

If the core genomes are available, the reference index necessary for abundance estimation can be created from it using the **`BIB_prepare_index`** file. The input required for this script are the set of core genomes and the name of the index to be generated.  For example, if the core genome file is called *core_genomes.fasta* and if the user wants the name of the index to be *`core_reference_index`*, then the command must be given as follows :

``python BIB_prepare_index.py core_genomes.fasta core_reference_index``

The alignment of the reads to this reference index and the estimation of the abundances of the strains from this alignment can then be estimated using the **`BIB_analyse_reads`** file. The input required for this script are the name of the readset, the core genomes used for the construction of the index and the name of the index. For example, if the readset is called *Sample_set.fastq*, the core genome file used for the creation of the index is called *core_genome.fasta* and the generated index is called *`core_reference_index`*, then the command must be given as follows :

``python BIB_analyse_reads.py Sample_set.fastq core_genome.fasta core_reference_index``

The output files produced contain the predicted abundances of the strains. These files will have the same name as the name of the readset given as the input to the script. For the above example, the output file would be produced as *`Sample_set.m_alpha`*.



