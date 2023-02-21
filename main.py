import streamlit as st
import pandas as pd
import plotly.express as px
import data_cleaning as dc
import datetime
import streamlit_nested_layout
from auth import get_authenticator, get_authentication_status
import streamlit_authenticator as stauth
from dateutil.relativedelta import relativedelta
from storage import upload_raw_df_as_excel


st.set_page_config(page_title= "Finance dashboard", page_icon = "🦈",layout = "wide")

dc.clean_from_raw_data()
df = dc.get_data()


authenticator = get_authenticator()

if get_authentication_status(authenticator):
    authenticator.logout('Logout', 'main')
    if df.empty:
        uploaded_file = st.file_uploader("Töltsd fel a tranzakciótörténetet:", type = "xlsx")
        if uploaded_file is not None:
            uploaded_df = pd.read_excel(uploaded_file)
            upload_raw_df_as_excel(df=uploaded_df, df_name=uploaded_file.name)
    else:

        filterchooser,fuploader3 = st.columns([2,1])
        with filterchooser:
            actual_filtered_df = dc.filter_dataframe_for_visualizations(df)

        with fuploader3:
            uploaded_file = st.file_uploader("Töltsd fel a tranzakciótörténetet:", type = "xlsx")
            if uploaded_file is not None:
                uploaded_df = pd.read_excel(uploaded_file)
                upload_raw_df_as_excel(df=uploaded_df, df_name=uploaded_file.name)

        income_and_spendings = dc.calculate_savings_and_spendings(actual_filtered_df)
        categories_income_and_spendings_with_date = dc.calculate_spendings_by_categories(actual_filtered_df)
        categories_income_and_spendings_with_date = categories_income_and_spendings_with_date[categories_income_and_spendings_with_date["Költési kategória"] != "Nem kategorizált"]
        categories_income_and_spendings_with_year_month = categories_income_and_spendings_with_date.drop(columns = ["Dátum"])
        #past_filtered_df_for_metric_delta = dc.calculate_savings_and_spendings(df,
        #    (min(actual_filtered_df['Könyvelés dátuma']) - relativedelta(months=1)), (max(actual_filtered_df['Könyvelés dátuma']) - relativedelta(months=1))
        #)
        past_spendings = dc.calculate_savings_and_spendings(past_filtered_df_for_metric_delta)

        categories_income_and_spendings_with_year_month.rename(columns={"YEAR":"Év", "MONTH":"Hónap"}, inplace = True)

        actual_filtered_df.drop(columns="Tranzakció dátuma", inplace = True)
        actual_filtered_df.rename(columns = {"Könyvelés dátuma":"Dátum"})

        fig = px.bar(categories_income_and_spendings_with_date, x = "Dátum", y = "Összeg", barmode = "group", color = "Költési kategória")
        fig.update_layout(xaxis=dict(tickformat="%Y-%m"))

        metr1, metr2 = st.columns(2)
        with st.container():
            metr1.metric("Bevétel", income_and_spendings["Bejövő"][0], delta=None, delta_color="normal", help=None, label_visibility="visible")
            metr2.metric("Költés", income_and_spendings["Kimenő"][0],
             delta=((income_and_spendings["Kimenő"][0] - past_spendings["Kimenő"][0]) / past_spendings["Kimenő"][0] * 100) , delta_color="inverse", help=None, label_visibility="visible")
            st.write("Tranzakciótörténet")
            st.dataframe(actual_filtered_df, use_container_width=True)

        st.markdown("---")

        st.write("Kategorikus kimutatás")
        categcol, graphcol = st.columns([1,2])
        with st.container():
            with categcol:
                st.dataframe(categories_income_and_spendings_with_year_month)
            with graphcol:
                st.plotly_chart(fig, theme = "streamlit", use_container_width=True)