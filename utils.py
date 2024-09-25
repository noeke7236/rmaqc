import datetime
import pytz
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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

def grafik_barang(data, kolom_tanggal, kolom_jumlah, judul, warna):
    data['Bulan'] = pd.to_datetime(data[kolom_tanggal], dayfirst=True).dt.strftime('%B')
    data['bulan'] = pd.to_datetime(data[kolom_tanggal], dayfirst=True).dt.month
    data['jumlah'] = 1
    result = data.groupby(['bulan']).agg(jumlah=('jumlah', 'count')).reset_index()

    no_bulan = [{'bulan': i, 'jumlah': 0} for i in range(1, 13)]
    data_bulan = pd.DataFrame(no_bulan)
    result_dataframe = pd.merge(data_bulan, result, on='bulan', how='left')
    result_dataframe['jumlah_y'] = result_dataframe['jumlah_y'].fillna(0).astype(int)

    max_value = result_dataframe['jumlah_y'].max()
    palette = ["#BEFF47" if y == max_value else warna for y in result_dataframe['jumlah_y']]

    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
    bar_plot = sns.barplot(data=result_dataframe, x="bulan", y="jumlah_y", palette=palette)
    ax_bar.set_xlabel('Bulan')
    ax_bar.set_ylabel('Jumlah barang')
    ax_bar.set_ylim(0, max_value + 50)

    for p in ax_bar.patches:
        height = p.get_height()
        ax_bar.annotate(f'{height:.0f}', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    ax_bar.set_xticks(range(len(month_names)))
    ax_bar.set_xticklabels([month_names[str(i)] for i in range(1, 13)], rotation=20)
    st.text("")
    st.subheader(judul)
    st.pyplot(fig_bar)
