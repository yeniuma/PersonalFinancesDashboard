import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import data_cleaning as dc
import datetime


st.set_page_config(page_title= "Finance dashboard", page_icon = "🦈",layout = "wide")

dtchooser1,dtchooser2,fuploader3 = st.columns(3)

with dtchooser1:
    start_date = st.date_input("Válassz időintervallumot", min_value=datetime.date(2022, 1, 1), max_value=datetime.date.today())
with dtchooser2:
    end_date = st.date_input("",min_value=datetime.date(2022, 1, 1), max_value=datetime.date.today())
with fuploader3:
    uploaded_file = st.file_uploader("Töltsd fel a tranzakció történetet", type = "xlsx")
    if uploaded_file is not None:
       uploaded_df = pd.read_excel(uploaded_file)
       uploaded_df.to_excel(f"../DataForFinanceDashboard/raw/{uploaded_file.name}")

df = dc.get_clean_data()
koltsegek = dc.calculate_savings_and_spendings(df,start_date, end_date)
filtered_df = dc.filter_df_by_date_range(df, start_date, end_date)

metr1, metr2, metr3 = st.columns(3)

st.table(koltsegek)

with st.container():
    metr1.metric("Bevétel", koltsegek["Bejövő"][0], delta=None, delta_color="normal", help=None, label_visibility="visible")
    metr2.metric("Költés", koltsegek["Kimenő"][0], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #col3.metric("Megtakarítás", (koltsegek["Bejövő"][0]-koltsegek["Kimenő"][0]), delta=None, delta_color="normal", help=None, label_visibility="visible")
    #st.dataframe(df, width = 1920)
    st.write("Tranzakciótörténet")
    st.dataframe(filtered_df, use_container_width=True)