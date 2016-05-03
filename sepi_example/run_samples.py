from __future__ import print_function
import sys
import os
from subprocess import call
from tqdm import tqdm

REFERENCEPATH = "/cs/work/scratch/ahonkela/bib/sepi/reference"
READPATH = "/cs/work/scratch/ahonkela/bib/sepi/Meric2015"

files = os.listdir(READPATH)
samples = [x[:-18] for x in files if x.endswith("_1_sequence.txt.gz")]

def make_readstring(stem):
    return "-1 %s/%s_1_sequence.txt.gz -2 %s/%s_2_sequence.txt.gz" % (READPATH, stem, READPATH, stem)

for s in tqdm(samples):
    with open(READPATH+"/"+s+".out", "w") as outf, open(READPATH+"/"+s+".err", "w") as errf:
        call("BIB_analyse_reads.py \"%s\" %s %s %s" %
             (make_readstring(s),
              REFERENCEPATH+"/Sepi_core_genomes.fasta",
              REFERENCEPATH+"/Sepi_core_genomes",
              READPATH+"/"+s),
             shell=True, stdout=outf, stderr=errf)
