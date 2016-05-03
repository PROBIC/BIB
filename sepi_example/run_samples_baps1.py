from __future__ import print_function
import sys
import os
from subprocess import call
from tqdm import tqdm
from itertools import islice

REFERENCEPATH = "/cs/work/scratch/ahonkela/bib/sepi/reference"
READPATH = "/cs/work/scratch/ahonkela/bib/sepi/Meric2015"

files = os.listdir(READPATH)
samples = [x[:-18] for x in files if x.endswith("_1_sequence.txt.gz")]

def make_readstring(stem):
    return "-1 %s/%s_1_sequence.txt.gz -2 %s/%s_2_sequence.txt.gz" % (READPATH, stem, READPATH, stem)

mystart = 0
mystep = 1
if len(sys.argv) > 2:
    mystart = int(sys.argv[1])
    mystep = int(sys.argv[2])

for s in tqdm(islice(samples, mystart, None, mystep)):
    with open(READPATH+"/"+s+"_BAPS1.out", "w") as outf, open(READPATH+"/"+s+"_BAPS1.err", "w") as errf:
        call("BIB_analyse_reads.py \"%s\" %s %s %s" %
             (make_readstring(s),
              REFERENCEPATH+"/Sepi_core_genomes_BAPS1.fasta",
              REFERENCEPATH+"/Sepi_core_genomes_BAPS1",
              READPATH+"/"+s+"_BAPS1"),
             shell=True, stdout=outf, stderr=errf)
