import os

import pandas as pd

blast_results_file = os.path.join("../data", "blast_results_50.csv")
df = pd.read.csv(blast_results_file)
