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

def total_barang_masuk(data):
    row_count, total_qty = calculate_statistics(data)
    tabel_barang = pd.DataFrame({'Kategori': ['Total Barang', 'Total Kuantitas'], 'Nilai': [row_count, total_qty]})
    st.subheader('Total Alat/Barang')
    st.markdown(tabel_barang.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    
# Load data
url = 'https://raw.githubusercontent.com/noeke7236/rmaqc/main/2023/2023.xlsx'
rma = load_data(url)
rma_modified = rma.copy()

url2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT85fb9TAXVvoVOWoBQ2kRJ_ETGs6DWyZ1u-ttnr8ejrvBvxC9yQvsVWRaKSRQkeSDC1SbPQJESmYqu/pub?output=xlsx'
rma2 = load_data(url2)
rma_modified2 = rma2.copy()
  
st.set_page_config(
    page_title="RMA&QC",
    page_icon=":watermelon:",
)

#st.sidebar.image("logo.png",use_column_width=True)

def rma_qc():
    st.markdown("# RMA QC ")
    st.sidebar.markdown("# RMA QC ")
    st.header('Alur Kerja', divider='rainbow')
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/rma_flowchart.png')
    st.text("")
    st.text("")
    st.header('Knowledge Base', divider='rainbow')
    url_link = "http://kb.mindotama.co.id/dokuwiki/doku.php?id=start"
    st.write("RMA QC Knowledge Base [link](%s)" % url_link)
    #st.markdown("check out this [link](%s)" % url)
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/webkbmindotama.png')
 
def rma_2023():
    st.markdown("# Infografis Tahun 2023")
    st.sidebar.markdown("# 2023 :bar_chart:")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Items", "1022")
    col2.metric("Total Quantity", "1935")
    col3.metric("Pass :heavy_check_mark:", "99.2%")
    col4.metric("Fail :x:", "0.8%")

    st.markdown("""---""")
    
    # TOTAL BARANG MASUK
    # Calculate statistics
    total_barang_masuk(rma_modified)
    #row_count, total_qty = calculate_statistics(rma_modified)
    #tabel_barang = pd.DataFrame({'Kategori': ['Total Barang', 'Total Kuantitas'], 'Nilai': [row_count, total_qty]})
    #st.subheader('Total Alat/Barang')
    #st.markdown(tabel_barang.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    # GRAFIK BARANG MASUK
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
    st.text("")
    st.subheader('Grafik barang masuk')
    # Display the barplot using st.pyplot()
    st.pyplot(fig_bar)

    # GRAFIK BARANG KELUAR
    rma_modified['Bulan_Keluar'] = pd.to_datetime(rma_modified['Tgl Selesai [PB07]'], dayfirst=True).dt.strftime('%B')
    rma_modified['bulan_out'] = pd.to_datetime(rma_modified['Tgl Selesai [PB07]'], dayfirst=True).dt.month

    rma_modified['jumlah_out'] = 1
    result_out = rma_modified.groupby(['bulan_out']).agg(jumlah_out=('jumlah_out', 'count')).reset_index()

    no_bulan_out = [{'bulan_out': i, 'jumlah_out': 0} for i in range(1, 13)]
    data_bulan_out = pd.DataFrame(no_bulan_out)

    # Menggabungkan dataframe result dan data_bulan berdasarkan kolom 'bulan'
    result_dataframe_out = pd.merge(data_bulan_out, result_out, on='bulan_out', how='left')
    
    # Mengisi nilai NaN dengan 0
    result_dataframe_out['jumlah_out_y'] = result_dataframe_out['jumlah_out_y'].fillna(0).astype(int)
    
    # Plot barplot
    fig_bar1, ax_bar1 = plt.subplots(figsize=(12, 6))
    bar_plot = sns.barplot(data=result_dataframe_out, x="bulan_out", y="jumlah_out_y", palette=["#FF6347" if y <= 200 else "#009EFA" for y in result_dataframe_out['jumlah_out_y']])
    ax_bar1.set_xlabel('Bulan')
    ax_bar1.set_ylabel('Jumlah barang')

    # Menambahkan batasan pada sumbu y
    ax_bar1.set_ylim(0, 400)

    # Menambahkan bar label
    for p in ax_bar1.patches:
        height = p.get_height()
        ax_bar1.annotate(f'{height:.0f}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    # Mengubah nilai sumbu x
    bulan_labels1 = ['Januari', 'Pebruari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'Nopember', 'Desember']
    ax_bar1.set_xticks(range(len(bulan_labels1)))
    ax_bar1.set_xticklabels(bulan_labels1, rotation=20)
    st.text("")
    st.subheader('Grafik barang keluar')
    # Display the barplot using st.pyplot()
    st.pyplot(fig_bar1)
    
    # PERSENTASE DALAM PROSES QC
    # Mengganti nilai 'OK' menjadi 'Good' dan 'NOK' menjadi 'Bad'
    rma_modified['Final Status Name'] = rma_modified['Final Status'].replace({'OK': 'Good', 'NOK': 'Bad'})
    
    # Result dari groupby dan value_counts
    result_counts = rma_modified.groupby(['RMA Level', 'Final Status Name'])['Final Status Name'].value_counts().unstack().fillna(0)
    result_counts = result_counts.applymap(lambda x: int(x) if x.is_integer() else x)

    # Result persentase
    result_percentage = (result_counts.div(result_counts.sum(axis=1), axis=0) * 100).round(1)

    # Membuat DataFrame
    tabel_persentase = pd.DataFrame({
        'Bad': result_counts['Bad'].astype(int),
        'Good': result_counts['Good'].astype(int),
        'Percentage Bad': result_percentage['Bad'],
        'Percentage Good': result_percentage['Good']
    })

    # Mengganti nama header 'Percentage Bad' dan 'Percentage Good'
    tabel_persentase = tabel_persentase.rename(columns={'Percentage Bad': 'Bad(%)', 'Percentage Good': 'Good(%)'})
    tabel_persentase.rename_axis(None, inplace=True)

    # Mengatur format angka desimal di kolom 'Percentage' menjadi 2 angka di belakang koma
    tabel_persentase['Bad(%)'] = tabel_persentase['Bad(%)'].apply(lambda x: f"{x:.1f}")
    tabel_persentase['Good(%)'] = tabel_persentase['Good(%)'].apply(lambda x: f"{x:.1f}")

    # Mengganti nama header 'RMA Level' menjadi 'Level'
    tabel_persentase.columns.name = 'Level'

    st.text("")
    st.subheader('Persentase dalam proses QC')
    st.markdown(tabel_persentase.style.to_html(), unsafe_allow_html=True)
    
    # Membuat Pie Chart untuk baris 'L1'
    fig_pie, ax_pie = plt.subplots()
    labels_pie = ['Bad', 'Good']
    colors_pie = ['#ff9999', '#66b3ff']
    explode_pie = (0.1, 0)  # memberikan efek explode pada slice pertama

    ax_pie.pie(tabel_persentase.loc['L1', ['Bad', 'Good']], explode=explode_pie, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    ax_pie.axis('equal')  # Pastikan lingkaran terlihat sebagai lingkaran

    # Menampilkan Pie Chart di Streamlit
    st.text("")
    st.subheader('Pie chart hasil proses QC')
    st.pyplot(fig_pie)

    #TABEL FAIL
    # Mencari data dengan kondisi Project == 'NOK' dan memilih kolom yang diinginkan
    filtered_data_nok = rma_modified.loc[rma_modified['Final Status'] == 'NOK', 
                                 ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 
                                  'Tgl Masuk [PB06]', 'Tgl Selesai [PB07]', 
                                  'Final Status', 'Project']]

    filtered_data_nok = filtered_data_nok.rename(columns={'RMA Level': 'Level', 'Final Status': 'Status'})
    # Menambahkan kolom index nomor urut
    filtered_data_nok['No.'] = range(1, len(filtered_data_nok) + 1)

    # Menyisipkan kolom 'No' sebelum kolom 'Nama Barang'
    filtered_data_nok.insert(0, 'No', filtered_data_nok.pop('No.'))

    # Menampilkan hasil di Streamlit
    st.text("")
    st.subheader('List beberapa Alat/Barang dengan status Bad/Fail setelah proses QC')
    st.markdown(filtered_data_nok.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    #TABEL LEVEL L3
    #Mencari data dengan kondisi RMA Level == L3 dan memilih kolom yang diinginkan
    filtered_data_L3 = rma_modified.loc[rma_modified['RMA Level'] == 'L3', 
                                 ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 
                                  'Tgl Masuk [PB06]', 'Tgl Selesai [PB07]', 
                                  'Final Status', 'Project']]

    filtered_data_L3 = filtered_data_L3.rename(columns={'RMA Level': 'Level', 'Final Status': 'Status'})
        
    # Menambahkan kolom index nomor urut
    filtered_data_L3['No.'] = range(1, len(filtered_data_L3) + 1)

    # Menyisipkan kolom 'No' sebelum kolom 'Nama Barang'
    filtered_data_L3.insert(0, 'No', filtered_data_L3.pop('No.'))
       
    # Menampilkan hasil di Streamlit
    st.text("")
    st.subheader('List Alat/Barang yang mengalami proses L3')
    st.markdown(filtered_data_L3.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        
    #GRAFIK BAR HORIZONTAL COUNT
    count_barang = rma_modified['Nama Barang'].value_counts().nlargest(10).sort_values(ascending=True)

    # Membuat horizontal bar chart
    fig_count, ax_count = plt.subplots()
    bars = count_barang.plot(kind='barh', color='skyblue')
    plt.xlabel('Jumlah')
    plt.ylabel('Alat/Barang')
    plt.grid(axis='x')

    # Menambahkan nilai di dalam setiap bar
    for bar, value in zip(bars.patches, count_barang):
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2 - 0.15, str(value), ha='center', va='center', color='black')

    # Menampilkan plot di Streamlit
    st.text("")
    st.subheader('Top 10 Alat/Barang berdasarkan jumlah item')
    st.pyplot(fig_count)

    #GRAFIK BAR HORIZONTAL SUM
    sum_barang = rma_modified.groupby('Nama Barang')['Qty'].sum().nlargest(10).sort_values(ascending=True)

    # Membuat horizontal bar chart dengan warna tomato
    fig_sum, ax_sum = plt.subplots()
    bars = sum_barang.plot(kind='barh', color='tomato')
    plt.xlabel('Jumlah')
    plt.ylabel('Alat/Barang')
    plt.grid(axis='x')

    # Menambahkan nilai di dalam setiap bar
    for bar, value in zip(bars.patches, sum_barang):
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2 - 0.15, str(value), ha='center', va='center', color='black')

    # Menampilkan plot di Streamlit
    st.text("")
    st.subheader('Top 10 Alat/Barang berdasarkan jumlah kuantitas')
    st.pyplot(fig_sum)

    # GRAFIK BAR PROJECT
    data_project = rma_modified['Project'].value_counts()

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

    # Menampilkan plot di Streamlit
    st.text("")
    st.subheader('Jumlah Alat/Barang berdasarkan project')
    st.pyplot(fig_bar2)

def rma_2024():
    st.markdown("# Infografis Tahun 2024")
    st.sidebar.markdown("# 2024 :bar_chart:")

    st.markdown("""---""")
    
    # TOTAL BARANG MASUK
    # Calculate statistics
    total_barang_masuk(rma_modified2)
    #row_count2, total_qty2 = calculate_statistics(rma_modified2)
    #tabel_barang2 = pd.DataFrame({'Kategori': ['Total Barang', 'Total Kuantitas'], 'Nilai': [row_count2, total_qty2]})
    #st.subheader('Total Alat/Barang')
    #st.markdown(tabel_barang2.style.hide(axis="index").to_html(), unsafe_allow_html=True)

#def page3():
#    st.markdown("# Page 3 🎉")
#    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "RMA QC": rma_qc,
    "2023": rma_2023,
    "2024": rma_2024
    #"Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
