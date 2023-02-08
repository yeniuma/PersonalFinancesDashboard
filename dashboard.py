import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import data_cleaning as dc
import datetime


st.set_page_config(page_title= "Finance dashboard", page_icon = "🦈",layout = "wide")

dtchooser,fuploader3 = st.columns(2)
categcol, graphcol = st.columns(2)
metr1, metr2, metr3 = st.columns(3)

with dtchooser:
    dts = st.date_input(label='Válassz időintervallumot: ',
                value=(datetime.date(2023, 1, 1), 
                        datetime.date(2023, 1, 2)),
                key='#date_range',
                help="Kezdő- és végdátum")

date_list = list(dts)
start_date = date_list[0]
if len(date_list) == 1:
    end_date = datetime.date.today()
else:
    end_date = date_list[1]

with fuploader3:
    uploaded_file = st.file_uploader("Töltsd fel a tranzakciótörténetet:", type = "xlsx")
    if uploaded_file is not None:
       uploaded_df = pd.read_excel(uploaded_file)
       uploaded_df.to_excel(f"../DataForFinanceDashboard/raw/{uploaded_file.name}")

df = dc.get_clean_data()
koltsegek = dc.calculate_savings_and_spendings(df,start_date, end_date)
filtered_df = dc.filter_df_by_date_range(df, start_date, end_date)
categories_spendings_with_date = dc.calculate_spendings_by_categories(df, start_date, end_date)
categories_spendings_with_year_month = categories_spendings_with_date.drop(columns = ["Dátum"])

categories_spendings_with_year_month.rename(columns={"YEAR":"Év", "MONTH":"Hónap"}, inplace = True)

st.table(koltsegek)

with st.container():
    metr1.metric("Bevétel", koltsegek["Bejövő"][0], delta=None, delta_color="normal", help=None, label_visibility="visible")
    metr2.metric("Költés", koltsegek["Kimenő"][0], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #col3.metric("Megtakarítás", (koltsegek["Bejövő"][0]-koltsegek["Kimenő"][0]), delta=None, delta_color="normal", help=None, label_visibility="visible")
    
    st.write("Tranzakciótörténet")
    st.dataframe(filtered_df, use_container_width=True)

with categcol:
    st.dataframe(categories_spendings_with_year_month)

fig = px.bar(categories_spendings_with_date, x = "Dátum", y = "Összeg", barmode = "group", color = "Költési kategória")
fig.update_layout(xaxis=dict(tickformat="%Y-%m"))

with graphcol:
    st.plotly_chart(fig, theme = "streamlit", use_container_width=True)