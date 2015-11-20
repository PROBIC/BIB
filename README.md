# BIB
Bayesian Identification of Bacteria


##Quick start for BIB for Staphylococcus aureus and Staphylococcus epidermidis

The following tools are required for the pipeline :

1. [Bowtie2](http://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.2.6/) - For the construction of the reference index and for the alignment of the reads.
2. [Bitseq](https://github.com/BitSeq/BitSeq) - For the estimation of the abundances from the alignment of the reads.

If the core genomes are available, the reference index necessary for
abundance estimation can be created from it using the
**`scripts/BIB_prepare_index.py`** script. The inputs required for this
script are the set of core genomes and the name of the index to be
generated.  For Staphylococcus aureus, the core genomes are provided as
*input/Aureus_core.fasta* and if the user wants the name of the index to be
*`input/Aureus_core`*, then the command must be given as follows :

``python scripts/BIB_prepare_index.py input/Aureus_core.fasta input/Aureus_core``

The alignment of the reads to this reference index and the estimation of the abundances of the strains from this alignment can then be estimated using the **`scripts/BIB_analyse_reads.py`** script. The input required for this script are the name of the readset, the core genomes used for the construction of the index and the name of the index. For example, if the readset is called *Sample_set.fastq*, the core genome file used for the creation of the index is called *input/Aureus_core.fasta* and the generated index is called *`input/Aureus_core`*, then the command must be given as follows :

``python scripts/BIB_analyse_reads.py Sample_set.fastq Aureus_core.fasta Aureus_core Sample_set_result``

The output files produced contain the predicted abundances of the strains. These files will have the same name as the name of the readset given as the input to the script. For the above example, the output file would be produced as *`Sample_set_result.m_alphas`*.


##General BIB pipeline

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

``parseAlignment  alignment_file.sam -o alignment_info.prob --trSeqFile core_alignment_gapless.fasta --trInfoFile genome_info.tr --uniform --verbose``

The alignment file produced in the previous step along with the gapless alignment of the core genomes is used as the input while the .prob file containing the probabilities of every alignment of each read and the .tr file containing the list of the genomes used to build the alignment file are produced as the outputs.

The second step estimates the relative transcript expression using a VB algorithm with the .prob file taken as the input.

``estimateVBExpression -o abundance alignment_info.prob -t genome_info.tr``

The sampler produces the file abundance.m_alphas which contains three columns. The first one corresponds to the estimated relative transcript expression levels (mean theta). The next two columns contain the parameters of the marginal Beta distribution describing the estimated distribution per transcript (alpha, beta). The resulting file will contains M lines, one for each transcript.
