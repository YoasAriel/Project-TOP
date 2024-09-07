import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import openpyxl
from streamlit_option_menu import option_menu
sns.set(style='dark')

# Title of the dashboard
st.set_page_config(
    page_title="TOP COMPUTER DASHBOARD", 
    page_icon="logo_top_white.jpg",
    layout="wide"
)

# Get Data From Excel
@st.cache_data
def  load_data():
    so_all_df = pd.read_excel("so_24.xlsx", engine="openpyxl")
    so_all_df['NET_SELLING'] = so_all_df.JL - so_all_df.RT
    so_all_df['QTY_TOTAL'] = so_all_df.qty_JUAL - so_all_df.qty_RETUR
    so_all_df['NET_PRICE'] = so_all_df.NET_SELLING / so_all_df.QTY_TOTAL
    return so_all_df
so_all_df = load_data()

def home():
    # Title
    st.title("CV. Tunggal Opti Persada - TOP Computer")
# Icon
    st.sidebar.image("logo_tunggal_utama_gelap.png", caption="THE BEST IT SOLUTION")

    # Sidebar for user input
    so_all_df["TGL_NOTA"] = pd.to_datetime(so_all_df["TGL_NOTA"])
    start_date = st.sidebar.date_input("Start Date", value=so_all_df["TGL_NOTA"].min(), format="DD/MM/YYYY")
    end_date = st.sidebar.date_input("End Date", value=so_all_df["TGL_NOTA"].max(), format="DD/MM/YYYY")
    line_selling = st.sidebar.multiselect(
        "Line Selling",
        options=so_all_df["LINE_SELLING"].unique(),
        default=so_all_df["LINE_SELLING"].unique()
    )
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
        "LINE_SELLING == @line_selling & TIPE_OUTLET == @tipe_outlet & CABANG == @cabang & KATEGORI == @kategori & MERK == @merk & PROCESSOR == @processor & TGL_NOTA >= @start_date & TGL_NOTA <= @end_date"
    )

    # KPI
    total_net_selling = int(so_all_df_selection["NET_SELLING"].sum())
    total_qty = int(so_all_df_selection["QTY_TOTAL"].sum())
    average_net_selling = round(so_all_df_selection["NET_SELLING"].mean(), 2)
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Revenue ")
        st.subheader(f"{total_net_selling:,}")
    with middle_column:
        st.subheader("Total QTY ")
        st.subheader(f"{total_qty:,}")
    with right_column:
        st.subheader("Average Revenue  ")
        st.subheader(f"{average_net_selling:,}")
        
    st.markdown("___")
    # Footer
    st.caption("Copyright © Yoas_Ariel 2024")

def table():
    # Icon
    st.sidebar.image("logo_tunggal_utama_gelap.png", caption="THE BEST IT SOLUTION")

    # Sidebar for user input
    so_all_df["TGL_NOTA"] = pd.to_datetime(so_all_df["TGL_NOTA"])
    start_date = st.sidebar.date_input("Start Date", value=so_all_df["TGL_NOTA"].min(), format="DD/MM/YYYY")
    end_date = st.sidebar.date_input("End Date", value=so_all_df["TGL_NOTA"].max(), format="DD/MM/YYYY")
    line_selling = st.sidebar.multiselect(
        "Line Selling",
        options=so_all_df["LINE_SELLING"].unique(),
        default=so_all_df["LINE_SELLING"].unique()
    )
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
        "LINE_SELLING == @line_selling & TIPE_OUTLET == @tipe_outlet & CABANG == @cabang & KATEGORI == @kategori & MERK == @merk & PROCESSOR == @processor & TGL_NOTA >= @start_date & TGL_NOTA <= @end_date"
    )


    st.title("CV. Tunggal Opti Persada - Summary")
    # KPI
    total_net_selling = int(so_all_df_selection["NET_SELLING"].sum())
    total_qty = int(so_all_df_selection["QTY_TOTAL"].sum())
    average_net_selling = round(so_all_df_selection["NET_SELLING"].mean(), 2)
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Revenue ")
        st.subheader(f"{total_net_selling:,}")
    with middle_column:
        st.subheader("Total QTY ")
        st.subheader(f"{total_qty:,}")
    with right_column:
        st.subheader("Average Revenue  ")
        st.subheader(f"{average_net_selling:,}")
        
    st.markdown("___")

    # TABLE BRANCH
    branch = so_all_df_selection.groupby(["CABANG"]).agg({
        "NET_SELLING": "sum",
        "QTY_TOTAL": "sum"
    }).sort_values(by="NET_SELLING", ascending=False)
    outlet = so_all_df_selection.groupby(["OUTLET"]).agg({
        "NET_SELLING": "sum"
    }).sort_values(by="NET_SELLING", ascending=False)
    sales = so_all_df_selection.groupby(["SALES"]).agg({
        "NET_SELLING": "sum"
    }).sort_values(by="NET_SELLING", ascending=False)
    left_column, middle_column, right_column = st.columns([3, 3, 2])
    with left_column:
        st.subheader("Branch")
        st.dataframe(branch)
    with middle_column:
        st.subheader("Outlet")
        st.dataframe(outlet)
    with right_column:
        st.subheader("Sales")
        st.dataframe(sales)

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

def dashboard():
# Icon
    st.sidebar.image("logo_tunggal_utama_gelap.png", caption="THE BEST IT SOLUTION")

    # Sidebar for user input
    so_all_df["TGL_NOTA"] = pd.to_datetime(so_all_df["TGL_NOTA"])
    start_date = st.sidebar.date_input("Start Date", value=so_all_df["TGL_NOTA"].min(), format="DD/MM/YYYY")
    end_date = st.sidebar.date_input("End Date", value=so_all_df["TGL_NOTA"].max(), format="DD/MM/YYYY")
    line_selling = st.sidebar.multiselect(
        "Line Selling",
        options=so_all_df["LINE_SELLING"].unique(),
        default=so_all_df["LINE_SELLING"].unique()
    )
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
        "LINE_SELLING == @line_selling & TIPE_OUTLET == @tipe_outlet & CABANG == @cabang & KATEGORI == @kategori & MERK == @merk & PROCESSOR == @processor & TGL_NOTA >= @start_date & TGL_NOTA <= @end_date"
    )

    st.title("Under Construction . . .")
    st.markdown("___")


# Menu
selected = option_menu(
        menu_title=None, #required
        options=["Home", "Table", "Dashboard"], #required
        icons=["house-door-fill", "table", "graph-up"], #optional
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "black"},
            "icon": {"color": "red", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "orange",
            },
            "nav-link-selected": {"background-color": "black"},
        },
    )

# Page
if selected == "Home":
    home()
if selected == "Table":
    table()
if selected == "Dashboard":
    dashboard()