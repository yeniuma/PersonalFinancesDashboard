import streamlit as st
import pandas as pd
import plotly.express as px
import data_cleaning as dc
import datetime
import streamlit_nested_layout


st.set_page_config(page_title= "Finance dashboard", page_icon = "🦈",layout = "wide")

filechooser,fuploader3 = st.columns([2,1])
categcol, graphcol = st.columns(2)
metr1, metr2, metr3 = st.columns(3)

df = dc.get_clean_data()

with filechooser:
    filtered_df = dc.filter_dataframe_for_visualizations(df)

with fuploader3:
    uploaded_file = st.file_uploader("Töltsd fel a tranzakciótörténetet:", type = "xlsx")
    if uploaded_file is not None:
       uploaded_df = pd.read_excel(uploaded_file)
       uploaded_df.to_excel(f"../DataForFinanceDashboard/raw/{uploaded_file.name}")

income_and_spendings = dc.calculate_savings_and_spendings(filtered_df)
#filtered_df = dc.filter_df_by_date_range(df, start_date, end_date)
categories_income_and_spendings_with_date = dc.calculate_spendings_by_categories(filtered_df)
categories_income_and_spendings_with_date = categories_income_and_spendings_with_date[categories_income_and_spendings_with_date["Költési kategória"] != "Nem kategorizált"]
categories_income_and_spendings_with_year_month = categories_income_and_spendings_with_date.drop(columns = ["Dátum"])

categories_income_and_spendings_with_year_month.rename(columns={"YEAR":"Év", "MONTH":"Hónap"}, inplace = True)

filtered_df.drop(columns="Tranzakció dátuma", inplace = True)
filtered_df.rename(columns = {"Könyvelés dátuma":"Dátum"})

with st.container():
    metr1.metric("Bevétel", income_and_spendings["Bejövő"][0], delta=None, delta_color="normal", help=None, label_visibility="visible")
    metr2.metric("Költés", income_and_spendings["Kimenő"][0], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #col3.metric("Megtakarítás", (income_and_spendings["Bejövő"][0]-income_and_spendings["Kimenő"][0]), delta=None, delta_color="normal", help=None, label_visibility="visible")
    
    st.write("Tranzakciótörténet")
    st.dataframe(filtered_df, use_container_width=True)

with categcol:
    st.dataframe(categories_income_and_spendings_with_year_month)

fig = px.bar(categories_income_and_spendings_with_date, x = "Dátum", y = "Összeg", barmode = "group", color = "Költési kategória")
fig.update_layout(xaxis=dict(tickformat="%Y-%m"))

with graphcol:
    st.plotly_chart(fig, theme = "streamlit", use_container_width=True)