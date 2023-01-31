import pandas as pd
import glob
import os

path = "Q:\Projects\DataForFinanceDashboard"
excel_files = glob.glob(os.path.join(path, "*.xlsx"))
processed_excels_path = os.path.join(path, "test.txt")

if os.path.exists(processed_excels_path):
    with open(processed_excels_path) as f:
        processed_excels = f.read().splitlines()
else:
    processed_excels = []

for f in excel_files:
    if f in processed_excels:
        continue
    df = pd.read_excel(f)

