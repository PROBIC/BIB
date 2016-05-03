from __future__ import print_function
import sys
import os
from subprocess import call
from tqdm import tqdm
import numpy as np
from openpyxl import load_workbook
import matplotlib.pyplot as plt

REFERENCEPATH = "/cs/work/scratch/ahonkela/bib/sepi/reference"
READPATH = "/cs/work/scratch/ahonkela/bib/sepi/Meric2015"
SAMPLEINFO = "/cs/work/scratch/ahonkela/bib/sepi/Meric et al Isolate Info.xlsx"
CLUSTER_INDEX = 1

CLUSTER_SIZES = [3, 11]

def read_table(fname, comment='#', sep=' '):
    lines = []
    with open(fname) as f:
        for l in f:
            if l.startswith(comment):
                continue
            lines.append(l.strip().split(sep))
    return np.array(lines)

def read_sample_mapping():
    wb = load_workbook(SAMPLEINFO)
    sheet = wb['SwanseaFastQ']
    val = dict()
    for j in range(2, 85):
        stem = sheet["E%d" % j].value[:-18]
        name = sheet["B%d" % j].value
        val[stem] = name
    return val


def read_clusters(index):
    clusters = read_table(REFERENCEPATH + "/sepi_genomes_and_clusters.txt", sep='\t')
    cl = dict()
    for c in clusters:
        cl[int(c[0][1:])] = int(c[1+index])
    return cl


def plot_boxplots(x1, x2):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(87.0/25.4, 70.0/25.4))
    plt.rcParams.update({'font.size': 6.0})
    ax1.boxplot(x1.flatten())
    ax2.boxplot(x2.flatten())
    for x in [ax1, ax2]:
        x.set_xticks(())
        x.set_ylabel("Estimated relative abundance")
    ax1.set_title("Correct cluster")
    ax2.set_title("Other clusters")


files = os.listdir(READPATH)
samples = [x[:-18] for x in files if x.endswith("_1_sequence.txt.gz")]

ids = read_sample_mapping()
clusters = read_clusters(CLUSTER_INDEX)

thetas = []
trueclusters = np.zeros(len(samples), np.int64)
trueclthetas = np.zeros(len(samples))
otherthetas = np.zeros((len(samples), CLUSTER_SIZES[CLUSTER_INDEX]-1))
for i, s in enumerate(tqdm(samples)):
    filestem = READPATH + "/" + s
    outfile = filestem + "_BAPS%d.m_alphas" % CLUSTER_INDEX
    trfile = filestem + "_BAPS%d.tr" % CLUSTER_INDEX

    trs = np.array(read_table(trfile))
    names = trs[:,1]
    allthetas = np.array(read_table(outfile)).astype(np.float64)
    thetas.append(allthetas[1:,0])
    trueclusters[i] = clusters[ids[s]]
    trueclthetas[i] = allthetas[trueclusters[i],0]
    otherthetas[i, :] = np.delete(allthetas[1:,0], trueclusters[i]-1)

thetas = np.stack(thetas, axis=1).T

refstrains = [int(x) for x in trs[:,1]]
samplestrains = [ids[x] for x in samples]
I = np.array(list(filter(lambda x: samplestrains[x] not in refstrains, range(len(samples)))))

plot_boxplots(trueclthetas, otherthetas)
plt.savefig("sepi_results_baps%d.pdf" % CLUSTER_INDEX)

plot_boxplots(trueclthetas[I], otherthetas[I,:])
plt.savefig("sepi_results_baps%d_filtered.pdf" % CLUSTER_INDEX)

print(np.sum(np.max(otherthetas[I,:], 1) < trueclthetas[I]), '/', len(I))
