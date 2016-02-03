from __future__ import print_function
import sys
import numpy as np

def read_table(fname, comment='#', sep=' '):
    lines = []
    with open(fname) as f:
        for l in f:
            if l.startswith(comment):
                continue
            lines.append(l.strip().split(sep))
    return np.array(lines)


if len(sys.argv) < 1:
    print("Print BIB abundance estimates in a simpler format.")
    print("Usage: python %s BIB_output_prefix" % sys.argv[0])
    sys.exit(1)

filestem = sys.argv[1]
outfile = filestem + ".m_alphas"
trfile = filestem + ".tr"

trs = np.array(read_table(trfile))
names = trs[:,1]
allthetas = np.array(read_table(outfile)).astype(np.float64)
thetas = allthetas[1:,0]
I = thetas.argsort()[::-1]

for k in I:
    print("%.03f\t%s" % (thetas[k], names[k]))

