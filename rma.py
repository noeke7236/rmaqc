# Contents of ~/rmaqc/rma.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#import pyecharts.options as opts
#from streamlit_echarts import st_pyecharts

#import streamlit_scrollable_textbox as stx
import plotly.graph_objects as go
import time

from tabulate import tabulate
from utils import get_current_time_in_jakarta
#from utils import load_data
from utils import drop_columns
from utils import normalize_columns
from utils import calculate_statistics
from utils import display_metrics
from utils import tabel_alat_barang
from utils import tampilkan_pie_chart
from utils import statistik_barang
from utils import grafik_barang
from utils import grafik_bar_project

from config import mylist
from config import columns_to_drop
from rma_qc import rma_qc
from rma_2022 import rma_2022
from rma_2023 import rma_2023
from rma_2024 import rma_2024
from rma_2025 import rma_2025

sns.set_theme(style="darkgrid")

st.set_page_config(
    page_title="QC & RMA",
    page_icon=":watermelon:",
)

st.markdown(f"<p style='font-size: 24px ; text-align: right'>{get_current_time_in_jakarta()}</p>", unsafe_allow_html=True)

#def calculate_percentage(data, column_name):
    # Hitung jumlah nilai unik
    #unique_counts = data[column_name].nunique()
    #print(f"Jumlah nilai unik: {unique_counts}")

    # Hitung jumlah untuk setiap status
    #status_counts = data[column_name].value_counts()
    #total_counts = status_counts.sum()

    #if unique_counts == 2:
        #good_counts = status_counts.get('OK', 0)
        #fail_counts = status_counts.get('NOK', 0)
        #good_percentage = (good_counts / total_counts * 100).round(1)
        #fail_percentage = (fail_counts / total_counts * 100).round(1)
        #return good_percentage, fail_percentage, None  # Tidak ada untested

    #elif unique_counts == 3:
        #good_counts = status_counts.get('OK', 0)
        #fail_counts = status_counts.get('NOK', 0)
        #untested_counts = status_counts.get('Untested', 0)
        #good_percentage = (good_counts / total_counts * 100).round(1)
        #fail_percentage = (fail_counts / total_counts * 100).round(1)
        #untested_percentage = (untested_counts / total_counts * 100).round(1)
        #return good_percentage, fail_percentage, untested_percentage

    #else:
        #raise ValueError("Jumlah nilai unik tidak didukung.")

def grafik_bar_horizontal_count(data):
    count_barang = data['Nama Barang'].value_counts().nlargest(10).sort_values(ascending=True)

    # Membuat horizontal bar chart
    fig_count, ax_count = plt.subplots()
    bars = count_barang.plot(kind='barh', color='skyblue', ax=ax_count)
    ax_count.set_xlabel('Jumlah')
    ax_count.set_ylabel('Alat/Barang')
    ax_count.grid(axis='x')

    # Menambahkan nilai di dalam setiap bar
    for bar, value in zip(bars.patches, count_barang):
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2 - 0.15, str(value), ha='center', va='center', color='black')

    # Menampilkan plot di Streamlit
    st.text("")
    st.subheader('Top 10 Alat/Barang berdasarkan jumlah item')
    st.pyplot(fig_count)

def grafik_bar_horizontal_sum(data):
    sum_barang = data.groupby('Nama Barang')['Qty'].sum().nlargest(10).sort_values(ascending=True)

    # Membuat horizontal bar chart dengan warna tomato
    fig_sum, ax_sum = plt.subplots()
    bars = sum_barang.plot(kind='barh', color='tomato', ax=ax_sum)
    ax_sum.set_xlabel('Jumlah')
    ax_sum.set_ylabel('Alat/Barang')
    ax_sum.grid(axis='x')

    # Menambahkan nilai di dalam setiap bar
    for bar, value in zip(bars.patches, sum_barang):
        ax_sum.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, str(value), ha='center', va='center', color='black')

    # Menampilkan plot di Streamlit
    st.text("")
    st.subheader('Top 10 Alat/Barang berdasarkan jumlah kuantitas')
    st.pyplot(fig_sum)

# Load data
#url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2gUwmQqoZnuheu3yON7gG9yep2apr1Hwcs9xvb4Ce1yxkIBNAHZmDoarWHOUymQ/pub?output=xlsx'
#rma = load_data(url)

#st.sidebar.image("logo.png",use_column_width=True)

#def rma_2023():
    #st.markdown("# Infografis Tahun 2023 :rabbit:")
    #st.sidebar.markdown("# 2023 :rabbit2:")

    #tahun = int(2023)
    
    #rma_modified = rma.copy()
    #rma_modified = drop_columns(rma_modified, columns_to_drop) #edit 02/08/2024
    #rma_modified = normalize_columns(rma_modified, mylist)
    
    #total_items, total_quantity = calculate_statistics(rma_modified)
    
    #good_percentage, fail_percentage, untested_percentage = calculate_percentage(rma_modified, 'Final Status')
    
    #display_metrics(total_items, total_quantity, good_percentage, fail_percentage, untested_percentage)

    #st.divider()
        
    # TOTAL BARANG MASUK
    # Calculate statistics
    #total_barang_masuk(rma_modified)
    #tabel_alat_barang(rma_modified)

    # PERSENTASE DALAM PROSES QC
    #tampilkan_pie_chart(good_percentage, fail_percentage, untested_percentage)
    
    # GRAFTIK BARANG MASUK DAN KELUAR [old]
    #data_masuk = statistik_barang(rma_modified, 'Tgl Masuk [PB06]', 'Barang Masuk', "#009EFA")
    #data_keluar = statistik_barang(rma_modified, 'Tgl Keluar [PB07]', 'Barang Keluar', "#FF6347")

    # GRAFTIK BARANG MASUK DAN KELUAR
    #data_masuk = statistik_barang(rma_modified, 'Tgl Masuk [PB06]', 'Barang Masuk', "#009EFA", tahun)
    #data_keluar = statistik_barang(rma_modified, 'Tgl Keluar [PB07]', 'Barang Keluar', "#FF6347", tahun)
    
    # Membuat grafik barang masuk dan keluar
    #bar = grafik_barang(data_masuk, data_keluar)
    # Menampilkan grafik di Streamlit
    #st.subheader("Grafik Barang Masuk dan Keluar")
    #st_pyecharts(bar, height="500px")
    
    # GRAFIK BARANG MASUK
    #grafik_barang(rma_modified, 'Tgl Masuk [PB06]', 'jumlah_in', 'Grafik barang masuk', "#009EFA")
        
    # GRAFIK BARANG KELUAR
    #grafik_barang(rma_modified, 'Tgl Keluar [PB07]', 'jumlah_out', 'Grafik barang keluar', "#FF6347")
    
    # PERSENTASE DALAM PROSES QC
    
    # Membuat Pie Chart untuk baris 'L1'
    #fig_pie, ax_pie = plt.subplots()
    #labels_pie = ['Bad', 'Good']
    #colors_pie = ['#ff9999', '#66b3ff']
    #explode_pie = (0.1, 0)  # memberikan efek explode pada slice pertama

    #ax_pie.pie(tabel_persentase.loc['L1', ['Bad', 'Good']], explode=explode_pie, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    #ax_pie.pie(tabel_persentase.loc['Bad', 'Good'], explode=explode_pie, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    #ax_pie.axis('equal')  # Pastikan lingkaran terlihat sebagai lingkaran

    # Menampilkan Pie Chart di Streamlit
    #st.text("")
    #st.subheader('Pie chart hasil proses QC')
    #st.pyplot(fig_pie)

    #TABEL FAIL
    # Mencari data dengan kondisi Project == 'NOK' dan memilih kolom yang diinginkan
    #filtered_data_nok = rma_modified.loc[rma_modified['Final Status'] == 'NOK', 
    #                             ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 
    #                              'Tgl Masuk [PB06]', 'Tgl Selesai [PB07]', 
    #                              'Final Status', 'Project']]

    #filtered_data_nok = filtered_data_nok.rename(columns={'RMA Level': 'Level', 'Final Status': 'Status'})
    # Menambahkan kolom index nomor urut
    #filtered_data_nok['No.'] = range(1, len(filtered_data_nok) + 1)

    # Menyisipkan kolom 'No' sebelum kolom 'Nama Barang'
    #filtered_data_nok.insert(0, 'No', filtered_data_nok.pop('No.'))

    # Menampilkan hasil di Streamlit
    #st.text("")
    #st.subheader('List beberapa Alat/Barang dengan status Bad/Fail setelah proses QC')
    #st.markdown(filtered_data_nok.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    #TABEL LEVEL L3
    #Mencari data dengan kondisi RMA Level == L3 dan memilih kolom yang diinginkan
    #filtered_data_L3 = rma_modified.loc[rma_modified['RMA Level'] == 'L3', 
    #                             ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 
    #                              'Tgl Masuk [PB06]', 'Tgl Selesai [PB07]', 
    #                              'Final Status', 'Project']]

    #filtered_data_L3 = filtered_data_L3.rename(columns={'RMA Level': 'Level', 'Final Status': 'Status'})
        
    # Menambahkan kolom index nomor urut
    #filtered_data_L3['No.'] = range(1, len(filtered_data_L3) + 1)

    # Menyisipkan kolom 'No' sebelum kolom 'Nama Barang'
    #filtered_data_L3.insert(0, 'No', filtered_data_L3.pop('No.'))
       
    # Menampilkan hasil di Streamlit
    #st.text("")
    #st.subheader('List Alat/Barang yang mengalami proses L3')
    #st.markdown(filtered_data_L3.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        
    #GRAFIK BAR HORIZONTAL COUNT
    #grafik_bar_horizontal_count(rma_modified)
    
    #GRAFIK BAR HORIZONTAL SUM
    #grafik_bar_horizontal_sum(rma_modified)
    
    # GRAFIK BAR PROJECT
    #grafik_bar_project(rma_modified, 'Project Tahun 2023')
    #grafik_bar_project(rma_modified)

page_names_to_funcs = {
    "QC & RMA": rma_qc,
    "2022": rma_2022,
    "2023": rma_2023,
    "2024": rma_2024,
    "2025": rma_2025
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
