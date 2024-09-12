import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
stock_df = pd.read_excel("stock.xlsx", engine="openpyxl")

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
        "PROCESSOR",
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
        "PROCESSOR",
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
        "PROCESSOR",
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
    st.title("Under Construction . . .")
    
    # Line Selling
    st.subheader("Total Revenue by Line Selling")
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September"]
    so_all_df_selection["Bulan"] = pd.Categorical(so_all_df_selection["Bulan"], categories=month_order, ordered=True)
    line_selling_df = so_all_df_selection.groupby(["LINE_SELLING", "Bulan"])["NET_SELLING"].sum().reset_index()
    st.line_chart(data=line_selling_df, x="Bulan", y="NET_SELLING", color="LINE_SELLING", use_container_width=True)
    
    # TOP 10 Category & Brand
    top10_category, top10_brand = st.columns(2)
    with top10_category:
        st.subheader("Top 10 by Category")
        top10_category_df = so_all_df_selection.groupby("KATEGORI")["NET_SELLING"].sum().sort_values(ascending=False).reset_index()
        plt.figure(figsize=(10,6))
        plt.bar(top10_category_df.sort_values(by="NET_SELLING", ascending=False).head(10)["KATEGORI"], top10_category_df.sort_values(by="NET_SELLING", ascending=False).head(10)["NET_SELLING"], color="skyblue")
        plt.title("Top 10 by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Revenue")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt.gcf())
    with top10_brand:
        st.subheader("Top 10 by Brand")
        top10_brand_df = so_all_df_selection.groupby("MERK")["NET_SELLING"].sum().sort_values(ascending=False).reset_index()
        top10_brand_df["MERK"] = top10_brand_df["MERK"].astype(str)
        plt.figure(figsize=(10,6))
        plt.bar(top10_brand_df.sort_values(by="NET_SELLING", ascending=False).head(10)["MERK"], top10_brand_df.sort_values(by="NET_SELLING", ascending=False).head(10)["NET_SELLING"], color="skyblue")
        plt.title("Top 10 by Brand")
        plt.xlabel("Brand")
        plt.ylabel("Total Revenue")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt.gcf())
    
    # Pie Chart

    # Footer
    st.caption("Copyright © Yoas_Ariel 2024")

def stock():
    # Title
    st.title("CV. Tunggal Opti Persada - TOP Computer")
    # Icon
    st.sidebar.image("logo_tunggal_utama_gelap.png", caption="THE BEST IT SOLUTION")
    select_all = st.checkbox("Select All Product")
    if select_all:
        product = stock_df["PRODUCT"]
    else:
        product = st.multiselect(
        "Select Product :",
        options=stock_df["PRODUCT"].unique(),
        default=[]
        )
    
    cabang = st.sidebar.multiselect(
        "CABANG",
        options=stock_df["CABANG"].unique(),
        default=stock_df["CABANG"].unique()
    )
    kategori = st.sidebar.multiselect(
        "KATEGORI",
        options=stock_df["KATEGORI"].unique(),
        default=stock_df["KATEGORI"].unique()
    )
    merk = st.sidebar.multiselect(
        "MERK",
        options=stock_df["MERK"].unique(),
        default=stock_df["MERK"].unique()
    )
    processor = st.sidebar.multiselect(
        "PROCESSOR",
        options=stock_df["PROCESSOR"].unique(),
        default=stock_df["PROCESSOR"].unique()
    )
    stock_df_selection = stock_df.query(
    "PRODUCT == @product & CABANG == @cabang & KATEGORI == @kategori & MERK == @merk & PROCESSOR == @processor"
    )

    # Product, Cabang DF
    stock_df_selection["MERK"] = stock_df_selection["MERK"].astype(str)
    stock_df_selection["PROCESSOR"] = stock_df_selection["PROCESSOR"].astype(str)
    product = stock_df_selection.groupby(["PRODUCT", "CABANG"]).agg({
        "QTY": "sum"
    }).sort_index(ascending=True)
    st.subheader("Product")
    st.dataframe(product, width=750, use_container_width=False)

    # Kategori, Merk, Processor DF
    kategori = stock_df_selection.groupby(["KATEGORI", "MERK", "PROCESSOR"]).agg({
        "QTY": "sum"
    }).sort_index(ascending=True)
    merk = stock_df_selection.groupby("MERK").agg({
        "QTY": "sum"
    }).sort_values(by="QTY", ascending=False)
    processor = stock_df_selection.groupby("PROCESSOR").agg({
        "QTY": "sum"
    }).sort_values(by="QTY", ascending=False)
    left_column, middle_column, right_column = st.columns([4, 1, 1])
    with left_column:
        st.subheader("Kategori")
        st.dataframe(kategori)
    with middle_column:
        st.subheader("Merk")
        st.dataframe(merk)
    with right_column:
        st.subheader("Processor")
        st.dataframe(processor)
    st.markdown("___")
    # Footer
    st.caption("Copyright © Yoas_Ariel 2024")

# Menu
selected = option_menu(
        menu_title=None,
        options=["Home", "Stock", "Table", "Dashboard"],
        icons=["house-door-fill", "box", "table", "graph-up"],
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
if selected == "Stock":
    stock()
if selected == "Table":
    table()
if selected == "Dashboard":
    dashboard()