# Contents of ~/rmaqc/rma.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")

def load_data(url):
    return pd.read_excel(url)

def calculate_statistics(data):
    row_count = len(data)
    total_qty = data['Qty'].sum()
    return row_count, total_qty


# Load data
url = 'https://raw.githubusercontent.com/noeke7236/rmaqc/main/2023/2023.xlsx'
rma = load_data(url)
rma_modified = rma.copy()

#rma = pd.read_excel('/main/2023/2023.xlsx')
  
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
    #total_qty = rma_modified['Qty'].sum()
    # Calculate statistics
    row_count, total_qty = calculate_statistics(rma_modified)
    tabel_barang = pd.DataFrame({'Kategori': ['Total Barang', 'Total Kuantitas'], 'Nilai': [row_count, total_qty]})
    st.subheader('Total barang yang masuk')
    st.markdown(tabel_barang.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    # Create a barplot
    rma_modified['Bulan_Masuk'] = pd.to_datetime(rma_modified['Tgl Masuk [PB06]'], dayfirst=True).dt.strftime('%B')
    rma_modified['bulan'] = pd.to_datetime(rma_modified['Tgl Masuk [PB06]'], dayfirst=True).dt.month
    rma_modified['jumlah'] = 1
    result = rma_modified.groupby(['bulan']).agg(jumlah=('jumlah', 'count')).reset_index()

    no_bulan = [{'bulan': i, 'jumlah': 0} for i in range(1, 13)]
    data_bulan = pd.DataFrame(no_bulan)
    result_dataframe = pd.merge(data_bulan, result, on='bulan', how='left')
    result_dataframe['jumlah_y'] = result_dataframe['jumlah_y'].fillna(0).astype(int)

    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
    bar_plot = sns.barplot(data=result_dataframe, x="bulan", y="jumlah_y", palette=["#009EFA" if y <= 200 else "#FF6347" for y in result_dataframe['jumlah_y']])
    ax_bar.set_xlabel('Bulan')
    ax_bar.set_ylabel('Jumlah barang')
    ax_bar.set_ylim(0, 400)

    for p in ax_bar.patches:
        height = p.get_height()
        ax_bar.annotate(f'{height:.0f}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    bulan_labels = ['Januari', 'Pebruari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'Nopember', 'Desember']
    ax_bar.set_xticks(range(len(bulan_labels)))
    ax_bar.set_xticklabels(bulan_labels, rotation=20)

    # Display the barplot using st.pyplot()
    st.pyplot(fig_bar)
        
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
