# Contents of ~/rmaqc/rma.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(url):
    return pd.read_excel(url)

def calculate_statistics(data):
    row_count = len(data)
    total_qty = data['Qty'].sum()
    return row_count, total_qty

def table_statistics(data):
    st.table(data, use_container_width=True, index_col=False)

# Load data
url = 'https://raw.githubusercontent.com/noeke7236/rmaqc/main/2023/2023.xlsx'
rma = load_data(url)
#rma = pd.read_excel('https://raw.githubusercontent.com/noeke7236/rmaqc/main/2023/2023.xlsx')
#rma = pd.read_excel('/main/2023/2023.xlsx')
rma_modified = rma.copy()
  
st.set_page_config(
    page_title="RMA&QC",
    page_icon=":watermelon:",
)

#st.sidebar.image("logo.png",use_column_width=True)

def rma_qc():
    st.markdown("# RMA QC 🎈")
    st.sidebar.markdown("# RMA QC 🎈")
    st.header('Alur Kerja', divider='rainbow')
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/rma_flowchart.png')
 
def rma_2023():
    st.markdown("# Statistik 2023")
    st.sidebar.markdown("# 2023 :tulip:")
    #row_count = len(rma_modified)
    #print("Total barang:",row_count)
    #rma_modified_qty = rma_modified['Qty'].sum()
    #print("Total kuantitas:", rma_modified_qty)
    # Calculate statistics
    row_count, total_qty = calculate_statistics(rma_modified)
    #tabel_barang = [['Total Barang', row_count], ['Total Kuantitas', rma_modified_qty]]
    tabel_barang = [['Total Barang', row_count], ['Total Kuantitas', total_qty]
    st.subheader('Total barang yang masuk')
    table_statistics(tabel_barang)
    #st.table(tabel_barang)

#def page3():
#    st.markdown("# Page 3 🎉")
#    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "RMA QC": rma_qc,
    "2023": rma_2023,
    #"Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
