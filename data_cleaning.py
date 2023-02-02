import pandas as pd
import glob
import os
import numpy as np

def read_list_of_already_processed_excels(path):
    if os.path.exists(path):
        with open(path) as f:
            t_list = f.read().splitlines()
    else:
        t_list = []
    return(t_list)    

def write_processsed_excels_name(path, processed_excels_list):
    with open(path, 'w') as f:
        for item in processed_excels_list:
            f.write("%s\n" % item)

def read_excels_if_not_already_processed(raw_excels, processed_excels_list):
    df = []
    for f in raw_excels:
        if f in processed_excels_list:
            continue
        processed_excels_list.append(f)
        temp = pd.read_excel(f, index_col=None, header=0)
        df.append(temp)
    dframe = pd.concat(df, axis=0, ignore_index=True)
    return(dframe)

path = "Q:\Projects\DataForFinanceDashboard"
raw_excel_files = glob.glob(os.path.join(path, "raw\*.xlsx"))
processed_excels_path = os.path.join(path, "processed_excels.txt")
compiled_excel_files= os.path.join(path, "clean")

processed_excels = read_list_of_already_processed_excels(processed_excels_path)

frame = read_excels_if_not_already_processed(raw_excel_files, processed_excels)

frame['Számla tulajdonos'] = np.where(frame['Számla szám'] == 1177337702327033, 'Adrienn', 'Botond')
frame['ID'] = frame['Tranzakció dátuma'] + frame['Partner neve'] + frame['Számla szám'].apply(str) + frame['Összeg'].apply(str)

frame.drop_duplicates(subset = "ID")

print(frame)

frame.to_excel(os.path.join(compiled_excel_files, "clean_df.xlsx"))

write_processsed_excels_name(processed_excels_path, processed_excels)