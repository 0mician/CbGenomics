import os

import pandas as pd
import numpy as np

blast_results_file = os.path.join("data", "blast_results_60.csv")
df = pd.read_csv(blast_results_file)

colnames_file = os.path.join("data", "gene_list.txt")
with open(colnames_file, "r") as f:
    colnames = f.read().splitlines()

rownames_file = os.path.join("data", "strains_list.txt")
with open(rownames_file, "r") as f:
    rownames = f.read().splitlines()

report = pd.DataFrame(0.0, index=rownames, columns=colnames)
print(report.ix["CC-1985"]["CBO0123"])

for index, row in df.iterrows():
    strain = df.ix[index]["strain"]
    gene = df.ix[index]["query"]
    value = df.ix[index]["ppos"]

    if(report.ix[strain][gene] < value):
        report.ix[strain][gene] = value

print(report.ix["CC-1985"]["CBO0123"])
report.to_csv("report_60.csv")
