# Contents of ~/rmaqc/rma.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_scrollable_textbox as stx
import plotly.graph_objects as go
import time

from tabulate import tabulate
from utils import get_current_time_in_jakarta
from utils import load_data
from utils import calculate_statistics
from utils import tabel_alat_barang
from utils import grafik_barang
from rma_2022 import rma_2022

sns.set_theme(style="darkgrid")

st.set_page_config(
    page_title="QC & RMA",
    page_icon=":watermelon:",
)

st.markdown(f"<p style='font-size: 24px ; text-align: right'>{get_current_time_in_jakarta()}</p>", unsafe_allow_html=True)

#edit 02/08/2024
def drop_columns(data, columns_to_drop):
    data.drop(columns_to_drop, axis=1, inplace=True)
    return data

def normalize_columns(data, target_columns):
    # Ambil nama kolom yang ada di DataFrame
    nama_kolom = data.columns.tolist()

    # Buat column_mapping secara otomatis berdasarkan perbedaan antara nama_kolom dan target_columns
    column_mapping = {nama_kolom[i]: target_columns[i] for i in range(min(len(nama_kolom), len(target_columns))) if nama_kolom[i] != target_columns[i]}

    # List untuk menyimpan nama kolom yang baru
    new_column_names = [column_mapping[col] if col in column_mapping else col for col in nama_kolom]

    # Ganti nama kolom di DataFrame
    data.columns = new_column_names
    return data

#def calculate_statistics(data):
#    row_count = len(data)
#    total_qty = data['Qty'].sum()
#    return row_count, total_qty

def calculate_percentage(data, column_name):
  # Mengganti nilai 'OK' menjadi 'Good' dan 'NOK' menjadi 'Bad'
  data[f'{column_name} Name'] = data[column_name].replace({'OK': 'Good', 'NOK': 'Bad'})

  # Hitung jumlah untuk setiap status
  status_counts = data[f'{column_name} Name'].value_counts()

  # Hitung persentase untuk setiap status
  total_counts = status_counts.sum()
  good_counts = status_counts.get('Good', 0)
  fail_counts = status_counts.get('Bad', 0)
  good_percentage = (good_counts / total_counts * 100).round(1)
  fail_percentage = (fail_counts / total_counts * 100).round(1)

  return good_counts, fail_counts, good_percentage, fail_percentage

def total_barang_masuk(data):
    row_count, total_qty = calculate_statistics(data)
    tabel_barang = pd.DataFrame({'Kategori': ['Total Barang', 'Total Kuantitas'], 'Nilai': [row_count, total_qty]})
    st.subheader('Total Alat/Barang')
    st.markdown(tabel_barang.style.hide(axis="index").to_html(), unsafe_allow_html=True)

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

def grafik_bar_project(data, title):
    data_project = data['Project'].value_counts()

    # Mengambil data dari Series data_project
    project_names = data_project.index
    project_counts = data_project.values

    # Membuat objek figure dan axes
    fig_bar2, ax_bar2 = plt.subplots(figsize=(12, 6))

    # Membuat bar plot dengan seaborn dan menggunakan axes
    sns.barplot(x=project_counts, y=project_names, palette='viridis', ax=ax_bar2)

    # Menambahkan bar label ke setiap batang
    for i, value in enumerate(project_counts):
        ax_bar2.text(value, i, f'{value}', ha='left', va='center', color='black')

    ax_bar2.set_ylabel('Project')
    ax_bar2.set_xlabel('Jumlah')
    ax_bar2.set_title(title)

    # Menampilkan plot di Streamlit
    st.text("")
    st.subheader('Jumlah Alat/Barang berdasarkan project')
    st.pyplot(fig_bar2)

# Load data
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2gUwmQqoZnuheu3yON7gG9yep2apr1Hwcs9xvb4Ce1yxkIBNAHZmDoarWHOUymQ/pub?output=xlsx'
rma = load_data(url)

url2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT85fb9TAXVvoVOWoBQ2kRJ_ETGs6DWyZ1u-ttnr8ejrvBvxC9yQvsVWRaKSRQkeSDC1SbPQJESmYqu/pub?output=xlsx'
rma2 = load_data(url2)
rma_modified2 = rma2.copy()

#url3 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQPxyl1P5AOFTBbTNR2f1TH3jP69HJigz2nnixuT2Ft3E67jeQFerdFoD5heO9YSY-Zi_H7TjHrTu3x/pub?output=xlsx'
#rma3 = load_data(url3)
#rma_modified3 = rma3.copy()

# List standar nama kolom
mylist = ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 'Tgl Masuk [PB06]', 'Tgl Keluar [PB07]', 'Final Status', 'Project']

# Kolom yang harus dihapus untuk data tahun 2023
columns_to_drop = ['Kategori','Expert','Tgl Tes','Tiket PB07']

#st.sidebar.image("logo.png",use_column_width=True)

def rma_qc():
    st.markdown("# QC & RMA ")
    st.sidebar.markdown("# QC & RMA ")
    st.header('Deskripsi', divider='rainbow')
    
    with open('deskripsi.txt', 'r') as file:
        deskripsi = file.read()
    stx.scrollableTextbox(deskripsi)
    
    st.header('Alur Kerja', divider='rainbow')
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/rma_flowchart.png')
    st.text("")
    st.text("")
    st.header('Knowledge Base', divider='rainbow')
    url_link = "http://kb.mindotama.co.id/dokuwiki/doku.php?id=start"
    st.write("QC & RMA Knowledge Base [link](%s)" % url_link)
    #st.markdown("check out this [link](%s)" % url)
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/webkbmindotama.png')

 def rma_2023():
    st.markdown("# Infografis Tahun 2023 :rabbit:")
    st.sidebar.markdown("# 2023 :rabbit2:")

    rma_modified = rma.copy()
    rma_modified = drop_columns(rma_modified, columns_to_drop) #edit 02/08/2024
    rma_modified = normalize_columns(rma_modified, mylist)
    
    total_items, total_quantity = calculate_statistics(rma_modified)
    good_counts, fail_counts, good_percentage, fail_percentage = calculate_percentage(rma_modified, 'Final Status')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Items", total_items)
    col2.metric("Total Quantity", total_quantity)
    col3.metric("Pass :heavy_check_mark:", f"{good_percentage:.1f}%")
    col4.metric("Fail :x:", f"{fail_percentage:.1f}%")

    st.markdown("""---""")
    
    # TOTAL BARANG MASUK
    # Calculate statistics
    #total_barang_masuk(rma_modified)
    tabel_alat_barang(rma_modified)
    
    # GRAFIK BARANG MASUK
    grafik_barang(rma_modified, 'Tgl Masuk [PB06]', 'jumlah_in', 'Grafik barang masuk', "#009EFA")
    #grafik_barang_masuk(rma_modified)
    
    # GRAFIK BARANG KELUAR
    grafik_barang(rma_modified, 'Tgl Keluar [PB07]', 'jumlah_out', 'Grafik barang keluar', "#FF6347")
    #grafik_barang_keluar(rma_modified)
    
    # PERSENTASE DALAM PROSES QC
    #edit 01/08/2024
    table_data = [
        ['Good', good_counts, good_percentage],
        ['Fail', fail_counts, fail_percentage]
      ]

    table_html = tabulate(table_data, headers=['Status', 'Total', 'Percentage(%)'], tablefmt='html')
    st.text("")
    st.subheader('Persentase dalam proses QC')
    st.markdown(table_html, unsafe_allow_html=True)

    #tabel_persentase = pd.DataFrame({
    #    'Bad': rma2023_counts['Bad'].astype(int),
    #    'Good': rma2023_counts['Good'].astype(int),
    #    'Bad(%)': rma2023_percentage['Bad'],
    #    'Good(%)': rma2023_percentage['Good']
    #})

    # Mengatur format angka desimal di kolom 'Percentage' menjadi 2 angka di belakang koma
    #tabel_persentase.rename_axis(None, inplace=True)
    #tabel_persentase['Bad(%)'] = tabel_persentase['Bad(%)'].apply(lambda x: f"{x:.1f}")
    #tabel_persentase['Good(%)'] = tabel_persentase['Good(%)'].apply(lambda x: f"{x:.1f}")
    
    # Mengganti nama header 'RMA Level' menjadi 'Level'
    #tabel_persentase.columns.name = 'Level'
    
    #st.markdown(tabel_persentase.style.to_html(), unsafe_allow_html=True)
    
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
    grafik_bar_horizontal_count(rma_modified)
    
    #GRAFIK BAR HORIZONTAL SUM
    grafik_bar_horizontal_sum(rma_modified)
    
    # GRAFIK BAR PROJECT
    grafik_bar_project(rma_modified, 'Project 2023')

def rma_2024():
    st.markdown("# Infografis Tahun 2024 :dragon_face:")
    st.sidebar.markdown("# 2024 :dragon:")

    #total_items2, total_quantity2 = calculate_statistics(rma_modified2)
    total_items, total_quantity = calculate_statistics(rma_modified2)
    good_counts, fail_counts, good_percentage, fail_percentage = calculate_percentage(rma_modified2, 'Final Status')
        
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Items", total_items)
    col2.metric("Total Quantity", total_quantity)
    col3.metric("Pass :heavy_check_mark:", f"{good_percentage:.1f}%")
    col4.metric("Fail :x:", f"{fail_percentage:.1f}%")

    st.markdown("""---""")
    
    # TOTAL BARANG MASUK
    #total_barang_masuk(rma_modified2)
    tabel_alat_barang(rma_modified2)

    # PERSENTASE DALAM PROSES QC
    #edit 01/08/2024
    table_data = [
        ['Good', good_counts, good_percentage],
        ['Fail', fail_counts, fail_percentage]
      ]

    table_html = tabulate(table_data, headers=['Status', 'Total', 'Percentage(%)'], tablefmt='html')
    st.text("")
    st.subheader('Persentase dalam proses QC')
    st.markdown(table_html, unsafe_allow_html=True)
    
    # GRAFIK BARANG MASUK
    #grafik_barang_masuk(rma_modified2)
    grafik_barang(rma_modified2, 'Tgl Masuk [PB06]', 'jumlah_in', 'Grafik barang masuk', "#009EFA")
    
    # GRAFIK BARANG KELUAR
    #grafik_barang_keluar(rma_modified2)
    grafik_barang(rma_modified2, 'Tgl Keluar [PB07]', 'jumlah_out', 'Grafik barang keluar', "#FF6347")

    #GRAFIK BAR HORIZONTAL COUNT
    grafik_bar_horizontal_count(rma_modified2)

    #GRAFIK BAR HORIZONTAL SUM
    grafik_bar_horizontal_sum(rma_modified2)

    # GRAFIK BAR PROJECT
    grafik_bar_project(rma_modified2, 'Project 2024')

page_names_to_funcs = {
    "QC & RMA": rma_qc,
    "2022": rma_2022,
    "2023": rma_2023,
    "2024": rma_2024
    #"Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
