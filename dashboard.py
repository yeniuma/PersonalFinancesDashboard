import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

path = "Q:\Projects\DataForFinanceDashboard\clean\clean_df.xlsx"
df = pd.read_excel(path)

st.checkbox("Use container width", value=False, key="use_container_width")

st.dataframe(df,use_container_width=st.session_state.use_container_width)