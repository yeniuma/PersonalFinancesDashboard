import pandas as pd
import glob
import os
import numpy as np

path = "Q:\Projects\DataForFinanceDashboard"
excel_files = glob.glob(os.path.join(path, "*.xlsx"))
processed_excels_path = os.path.join(path, "processed_excels.txt")

df = []

if os.path.exists(processed_excels_path):
    with open(processed_excels_path) as f:
        processed_excels = f.read().splitlines()
else:
    processed_excels = []

for f in excel_files:
    if f in processed_excels:
        continue
    processed_excels.append(f)
    temp = pd.read_excel(f, index_col=None, header=0)
    df.append(temp)

frame = pd.concat(df, axis=0, ignore_index=True)

frame['Számla tulajdonos'] = np.where(frame['Számla szám'] == 1177337702327033, 'Adrienn', 'Botond')
frame['ID'] = frame['Tranzakció dátuma'] + frame['Partner neve'] + str(frame['Számla szám']) + str(frame['Összeg'])

frame.drop_duplicates(subset = "ID")

print(frame)

with open(processed_excels_path, 'w') as f:
    for item in processed_excels:
        f.write("%s\n" % item)