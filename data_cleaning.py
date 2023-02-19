import pandas as pd
import glob
import os
import numpy as np
from datetime import datetime
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import streamlit as st

def read_list_of_already_processed_excels(path):
    if os.path.exists(path):
        with open(path) as f:
            t_list = f.read().splitlines()
    else:
        t_list = []
    return t_list     

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
    return dframe

def setup_data_directories():
    folders = ["DataForFinanceDashboard","DataForFinanceDashboard/raw","DataForFinanceDashboard/clean"]
    for f in folders:
        if not os.path.exists(f"../{f}"):
            os.mkdir(f"../{f}")

    if not os.path.exists("DataForFinanceDashboard/processed_excels.txt"):
        with open("processed_excels.txt", mode = "w"):
            pass

def clean_data():
    setup_data_directories()

    path = "..\DataForFinanceDashboard"
    raw_excel_files = glob.glob(os.path.join(path, "raw\*.xlsx"))
    processed_excels_path = os.path.join(path, "processed_excels.txt")
    compiled_excel_files= os.path.join(path, "clean")

    processed_excels = read_list_of_already_processed_excels(processed_excels_path)

    frame = read_excels_if_not_already_processed(raw_excel_files, processed_excels)

    frame['Számla tulajdonos'] = np.where(frame['Számla szám'] == 1177337702327033, 'Adrienn', 'Botond')
    frame['ID'] = frame['Tranzakció dátuma'] + frame['Partner neve'] + frame['Számla szám'].apply(str) + frame['Összeg'].apply(str)

    frame.drop_duplicates(subset = "ID")

    frame.drop(columns=["ID", "Számla név", "Számla szám", "Partner számlaszáma/azonosítója"], inplace=True)

    frame.to_excel(os.path.join(compiled_excel_files, f"clean_df{datetime.now()}.xlsx"), index=False)

    write_processsed_excels_name(processed_excels_path, processed_excels)

def get_clean_data():
    try:
        path = "..\DataForFinanceDashboard\clean\clean_df.xlsx"
        df = pd.read_excel(path)
    except FileNotFoundError:
        return pd.DataFrame()
    return df

def calculate_savings_and_spendings(df):
    df['Tranzakció dátuma'] = pd.to_datetime(df['Tranzakció dátuma'], errors='coerce')
    df['Könyvelés dátuma'] = pd.to_datetime(df['Tranzakció dátuma']).dt.date

    koltsegek = df#[(df['Könyvelés dátuma']>=start_date) & (df['Könyvelés dátuma']<=end_date)] 

    koltsegek = koltsegek.groupby(["Bejövő/Kimenő"])["Összeg"].sum().reset_index()
    koltsegek = pd.pivot_table(koltsegek, values = "Összeg", columns= "Bejövő/Kimenő").reset_index()
    koltsegek["Bejövő"], koltsegek["Kimenő"] = koltsegek.get('Bejövő', 0), koltsegek.get('Kimenő', 0) 
    koltsegek["Kimenő"] = koltsegek["Kimenő"]*-1
    koltsegek.loc[:, "Bejövő"], koltsegek.loc[:, "Kimenő"] = koltsegek["Bejövő"].map('{:,d}'.format), koltsegek["Kimenő"].map('{:,d}'.format)

    return koltsegek

def calculate_spendings_by_categories(df):
    df['Tranzakció dátuma'] = pd.to_datetime(df['Tranzakció dátuma'], errors='coerce')
    df['Könyvelés dátuma'] = pd.to_datetime(df['Tranzakció dátuma']).dt.date
    
    #kategoriak = koltsegek["Költési kategória"].unique().tolist()

    df = df.groupby(["Költési kategória",df['Tranzakció dátuma'].dt.year.rename('YEAR'), df['Tranzakció dátuma'].dt.month.rename('MONTH')])["Összeg"].sum().reset_index()
    df["Összeg"] = df["Összeg"]*-1 
    df["Dátum"] = pd.to_datetime(df[['YEAR', 'MONTH']].assign(DAY=1))
    return df

def filter_df_by_date_range(df, start_date, end_date):
    df['Könyvelés dátuma'] = pd.to_datetime(df['Tranzakció dátuma']).dt.date
    filtered_df = df[(df['Könyvelés dátuma']>=start_date) & (df['Könyvelés dátuma']<=end_date)]
    filtered_df.drop(columns= "Könyvelés dátuma", inplace= True)
    filtered_df['Tranzakció dátuma'] = filtered_df['Tranzakció dátuma'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    return filtered_df

def filter_dataframe_for_visualizations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
  
    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()
    

    with modification_container:
        
        to_filter_columns = st.multiselect("Szűrőfeltételek:", df.drop(columns = "Tranzakció dátuma").columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with <= 11 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() <= 11:
                user_cat_input = right.multiselect(
                    f"A {column} értékei",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"A {column} értékei",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"A {column} értékei",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Szubsztring vagy regex a {column} oszlopban",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df