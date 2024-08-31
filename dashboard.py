import numpy as np
import pandas as pd
import streamlit as st
sns.set(style='dark')

# Title of the dashboard
st.set_page_config(
    page_title="TOP COMPUTER DASHBOARD", 
    page_icon="logo_top_white.jpg",
    layout="wide"
)
st.title("CV. Tunggal Opti Persada Dashboard")

# Get Data From Excel
@st.cache_data
def  load_data():
    so_all_df = pd.read_excel("so_24.xlsx")
    so_all_df['NET_SELLING'] = so_all_df.JL - so_all_df.RT
    so_all_df['QTY_TOTAL'] = so_all_df.qty_JUAL - so_all_df.qty_RETUR
    so_all_df['NET_PRICE'] = so_all_df.NET_SELLING / so_all_df.QTY_TOTAL
    return so_all_df
so_all_df = load_data()

# Sidebar for user input
st.sidebar.header("Menu")
tipe_outlet = st.sidebar.multiselect(
    "Tipe Outlet",
    options=so_all_df["TIPE_OUTLET"].unique(),
    default=so_all_df["TIPE_OUTLET"].unique()
)
cabang = st.sidebar.multiselect(
    "CABANG",
    options=so_all_df["CABANG"].unique(),
    default=so_all_df["CABANG"].unique()
)
kategori = st.sidebar.multiselect(
    "KATEGORI",
    options=so_all_df["KATEGORI"].unique(),
    default=so_all_df["KATEGORI"].unique()
)
merk = st.sidebar.multiselect(
    "MERK",
    options=so_all_df["MERK"].unique(),
    default=so_all_df["MERK"].unique()
)
processor = st.sidebar.multiselect(
    "MERK",
    options=so_all_df["PROCESSOR"].unique(),
    default=so_all_df["PROCESSOR"].unique()
)

so_all_df_selection = so_all_df.query(
    "TIPE_OUTLET == @tipe_outlet & CABANG == @cabang & KATEGORI == @kategori & MERK == @merk & PROCESSOR == @processor"
)

# KPI
total_net_selling = int(so_all_df_selection["NET_SELLING"].sum())
total_qty = int(so_all_df_selection["QTY_TOTAL"].sum())
average_net_selling = round(so_all_df_selection["NET_SELLING"].mean(), 2)
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Net Selling ")
    st.subheader(f"{total_net_selling:,}")
with middle_column:
    st.subheader("Total QTY :")
    st.subheader(f"{total_qty:,}")
with right_column:
    st.subheader("Average Net Selling  ")
    st.subheader(f"{average_net_selling:,}")
    
st.markdown("___")
st.subheader("Cabang")

# TABLE BRANCH
branch = so_all_df_selection.groupby(["LINE_SELLING", "CABANG"]).agg({
    "NET_SELLING": "sum",
    "QTY_TOTAL": "sum"
})
st.dataframe(branch)

# TABLE PRODUCT
kategori = so_all_df_selection.groupby("KATEGORI").agg({
    "NET_SELLING": "sum",
    "QTY_TOTAL": "sum"
}).sort_values(by="NET_SELLING", ascending=False)
merk = so_all_df_selection.groupby("MERK").agg({
    "NET_SELLING": "sum",
    "QTY_TOTAL": "sum"
}).sort_values(by="NET_SELLING", ascending=False)
processor = so_all_df_selection.groupby("PROCESSOR").agg({
    "NET_SELLING": "sum",
    "QTY_TOTAL": "sum"
}).sort_values(by="NET_SELLING", ascending=False)
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Kategori")
    st.dataframe(kategori)
with middle_column:
    st.subheader("Merk")
    st.dataframe(merk)
with right_column:
    st.subheader("Processor")
    st.dataframe(processor)






# Footer
st.caption("Copyright © Yoas_Ariel 2024")
