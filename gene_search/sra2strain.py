import os
import re

import pandas as pd
import numpy as np

sra2strain_file = os.path.join("data", "strains_srr_dictionary.txt")
df = pd.read_csv(sra2strain_file, header=0)

pattern = re.compile('SRR[0-9]*')
newick = os.path.join("data", "cb.newick")
with open(newick, "r") as f:
    s = f.read()
    for match in re.findall(pattern, s):
        row_index = df.SRR[df.SRR == match].index.tolist()[0]
        s = s.replace(match, df.Strain[row_index])
    print(s)


