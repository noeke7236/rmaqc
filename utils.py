import datetime
import pytz
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go

from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts

# Month_names dictionary
month_names = {
    '1': 'Januari',
    '2': 'Februari',
    '3': 'Maret',
    '4': 'April',
    '5': 'Mei',
    '6': 'Juni',
    '7': 'Juli',
    '8': 'Agustus',
    '9': 'September',
    '10': 'Oktober',
    '11': 'November',
    '12': 'Desember'
}

def get_current_time_in_jakarta():
    jakarta_time = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    time_string = jakarta_time.strftime(f'{jakarta_time.day} {month_names[jakarta_time.strftime("%m").lstrip("0")]} {jakarta_time.year}')
    return time_string

def load_data(url):
    return pd.read_excel(url)

def drop_columns(data, columns_to_drop):
    data.drop(columns_to_drop, axis=1, inplace=True)
    return data

def normalize_columns(data, target_columns):
    nama_kolom = data.columns.tolist()
    column_mapping = {nama_kolom[i]: target_columns[i] for i in range(min(len(nama_kolom), len(target_columns))) if nama_kolom[i] != target_columns[i]}
    new_column_names = [column_mapping[col] if col in column_mapping else col for col in nama_kolom]
    data.columns = new_column_names
    return data

def calculate_statistics(data):
    row_count = len(data)
    total_qty = data['Qty'].sum()
    return row_count, total_qty

def calculate_percentage(data, column_name):
    # Hitung jumlah nilai unik
    unique_counts = data[column_name].nunique()
    #print(f"Jumlah nilai unik: {unique_counts}")

    # Hitung jumlah untuk setiap status
    status_counts = data[column_name].value_counts()
    total_counts = status_counts.sum()

    if unique_counts == 2:
        good_counts = status_counts.get('OK', 0)
        fail_counts = status_counts.get('NOK', 0)
        good_percentage = (good_counts / total_counts * 100).round(1)
        fail_percentage = (fail_counts / total_counts * 100).round(1)
        return good_percentage, fail_percentage, None  # Tidak ada untested

    elif unique_counts == 3:
        good_counts = status_counts.get('OK', 0)
        fail_counts = status_counts.get('NOK', 0)
        untested_counts = status_counts.get('Untested', 0)
        good_percentage = (good_counts / total_counts * 100).round(1)
        fail_percentage = (fail_counts / total_counts * 100).round(1)
        untested_percentage = (untested_counts / total_counts * 100).round(1)
        return good_percentage, fail_percentage, untested_percentage

    else:
        raise ValueError("Jumlah nilai unik tidak didukung.")

def display_metrics(total_items, total_quantity, good_percentage, fail_percentage, untested_percentage=None):
    unique_counts = 2 if untested_percentage is None else 3

    if unique_counts == 2:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Items", total_items)
        col2.metric("Total Quantity", total_quantity)
        col3.metric("Pass :heavy_check_mark:", f"{good_percentage:.1f}%")
        col4.metric("Fail :x:", f"{fail_percentage:.1f}%")

    elif unique_counts == 3:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Items", total_items)
        col2.metric("Total Quantity", total_quantity)
        col3.metric("Pass :heavy_check_mark:", f"{good_percentage:.1f}%")
        col4.metric("Untested :no_entry_sign:", f"{untested_percentage:.1f}%")
        col5.metric("Fail :x:", f"{fail_percentage:.1f}%")

def tabel_alat_barang(data):
    total_items, total_quantity = calculate_statistics(data)
    header = ['Total', 'Jumlah']
    data = [['Items', 'Quantity'], [total_items, total_quantity]]

    fig = go.Figure(data=[go.Table(
        columnwidth = [100,100],
        header=dict(values=header,
        fill_color='lightskyblue',
        align='center',
        font_size=24
        ),
        cells=dict(values=data,
        fill_color='lightcyan',
        align='center',
        height=30,
        font_size=20
        ),
    )
    ])

    fig.update_layout(
        width=300,
        height=100,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )

    st.subheader('Total Alat / Barang')
    st.plotly_chart(fig)

def statistik_barang(data, kolom_tanggal, judul, warna):
    data['Bulan'] = pd.to_datetime(data[kolom_tanggal], dayfirst=True).dt.strftime('%B')
    data['bulan'] = pd.to_datetime(data[kolom_tanggal], dayfirst=True).dt.month
    data['jumlah'] = 1
    result = data.groupby(['bulan']).agg(jumlah=('jumlah', 'count')).reset_index()

    no_bulan = [{'bulan': i, 'jumlah': 0} for i in range(1, 13)]
    data_bulan = pd.DataFrame(no_bulan)
    result_dataframe = pd.merge(data_bulan, result, on='bulan', how='left')
    result_dataframe['jumlah_y'] = result_dataframe['jumlah_y'].fillna(0).astype(int)

    return result_dataframe

def grafik_barang(data_masuk, data_keluar):
    bar = (
        Bar()
        .add_xaxis([month_names[str(i)] for i in range(1, 13)])
        .add_yaxis("Barang Masuk", data_masuk['jumlah_y'].tolist(), color="#009EFA")
        .add_yaxis("Barang Keluar", data_keluar['jumlah_y'].tolist(), color="#FF6347")
        .set_global_opts(
            #title_opts=opts.TitleOpts(title=judul),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
        )
    )
    return bar

#def grafik_barang(data, kolom_tanggal, kolom_jumlah, judul, warna):
    #data['Bulan'] = pd.to_datetime(data[kolom_tanggal], dayfirst=True).dt.strftime('%B')
    #data['bulan'] = pd.to_datetime(data[kolom_tanggal], dayfirst=True).dt.month
    #data['jumlah'] = 1
    #result = data.groupby(['bulan']).agg(jumlah=('jumlah', 'count')).reset_index()

    #no_bulan = [{'bulan': i, 'jumlah': 0} for i in range(1, 13)]
    #data_bulan = pd.DataFrame(no_bulan)
    #result_dataframe = pd.merge(data_bulan, result, on='bulan', how='left')
    #result_dataframe['jumlah_y'] = result_dataframe['jumlah_y'].fillna(0).astype(int)

    #max_value = result_dataframe['jumlah_y'].max()
    #palette = ["#BEFF47" if y == max_value else warna for y in result_dataframe['jumlah_y']]

    #fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
    # Tanggal 04102024
    #bar_plot = sns.barplot(data=result_dataframe, x="bulan", y="jumlah_y", hue="bulan", palette=palette, ax=ax_bar, legend=False)
    # Tanggal 04102024
    #ax_bar.set_xlabel('Bulan')
    #ax_bar.set_ylabel('Jumlah barang')
    #ax_bar.set_ylim(0, max_value + 50)

    #for p in ax_bar.patches:
        #height = p.get_height()
        #ax_bar.annotate(f'{height:.0f}', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    #ax_bar.set_xticks(range(len(month_names)))
    #ax_bar.set_xticklabels([month_names[str(i)] for i in range(1, 13)], rotation=20)
    #st.text("")
    #st.subheader(judul)
    #st.pyplot(fig_bar)

def total_barang_masuk(data):
    row_count, total_qty = calculate_statistics(data)
    tabel_barang = pd.DataFrame({'Kategori': ['Total Barang', 'Total Kuantitas'], 'Nilai': [row_count, total_qty]})
    st.subheader('Total Alat/Barang')
    st.markdown(tabel_barang.style.hide(axis="index").to_html(), unsafe_allow_html=True)

def grafik_bar_project(data, title):
    data_project = data['Project'].value_counts()

    # Mengambil data dari Series data_project dan membalikkan urutannya
    project_names = data_project.index[::-1]  # Membalik urutan nama project
    project_counts = data_project.values[::-1]  # Membalik urutan jumlah project
    
    # Membuat objek figure dan axes
    fig_bar2, ax_bar2 = plt.subplots(figsize=(12, 6))
    
    norm = plt.Normalize(project_counts.min(), project_counts.max())
    cmap = plt.get_cmap("viridis")
       
    # Membuat warna untuk setiap batang
    colors = [cmap(norm(count)) for count in project_counts]

    # Membuat bar plot menggunakan Matplotlib
    bars = ax_bar2.barh(project_names, project_counts, color=colors)

    # Menambahkan label ke setiap batang
    for bar in bars:
        width = bar.get_width()
        ax_bar2.text(width, bar.get_y() + bar.get_height()/2, f'{width}', ha='left', va='center', color='black')

    ax_bar2.set_ylabel('Project')
    ax_bar2.set_xlabel('Jumlah')
    ax_bar2.set_title(title)

    # Menampilkan plot di Streamlit
    st.text("")
    st.subheader('Jumlah Alat/Barang berdasarkan project')
    st.pyplot(fig_bar2)
