from __future__ import print_function
import sys
import os
from subprocess import call
import numpy as np
import numpy.random as npr

REFERENCEPATH = "/home/group/mlb/bib/sepi/reference"
# which clustering to use (0 = 3 clusters, 1 = 11 clusters)
CLUSTERING_INDEX = 1

DATABASE_NAME = "Sepi_core_genomes_BAPS%d" % CLUSTERING_INDEX

DATABASE_RAW = REFERENCEPATH + "/" + DATABASE_NAME + "_raw.fasta"
DATABASE_OUT = REFERENCEPATH + "/" + DATABASE_NAME + ".fasta"

npr.seed(42)

with open(REFERENCEPATH + "/EpiNewBAPS.partition.txt") as f:
    baps_clusters = [[int(t) for t in x.strip().split()] for x in f.readlines()]
clusters = np.array(baps_clusters)

with open(REFERENCEPATH + "/sepi_genome_names.txt") as f:
    genome_names = [x.strip() for x in f.readlines()]
genomes = np.array(genome_names)

names = np.array(genome_names)

myclusters = np.unique(clusters[:,CLUSTERING_INDEX])

# select random representative genomes for each cluster
mygenomes = []
for k in myclusters:
    mygenomes.append(genomes[npr.choice((clusters[:,CLUSTERING_INDEX] == k).nonzero()[0])])

# extract the references for the genomes
for k in mygenomes:
    call("~/github/BitSeq/fastagrep.sh '%s' %s >> %s" % (k, REFERENCEPATH + "/BIGSdb_15746_1383675596_44116.fas", DATABASE_RAW), shell=True)

# remove gaps from the reference
call("cat %s | tr -d - | tr -s \\\\n > %s" % (DATABASE_RAW, DATABASE_OUT), shell=True)

os.unlink(DATABASE_RAW)
