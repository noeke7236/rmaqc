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

def calculate_statistics(data):
    row_count = len(data)
    total_qty = data['Qty'].sum()
    return row_count, total_qty

def calculate_percentage(data):
    # Mengganti nilai 'OK' menjadi 'Good' dan 'NOK' menjadi 'Bad'
    data['Final Status Name'] = data['Final Status'].replace({'OK': 'Good', 'NOK': 'Bad'})

    # Menghitung nilai count untuk setiap kategori
    my_data_status = data['Final Status Name'].value_counts()

    # Membuat tabel dengan persentase
    table_data = {
      'Status': my_data_status.values,
      'Total': my_data_status.values,
      'Persentase': (my_data_status / my_data_status.sum() * 100).round(1)
    }
    percentage_table = pd.DataFrame(table_data)

    # Hitung persentase keseluruhan
    total_good = my_data_status.get('Good', 0)
    total_bad = my_data_status.get('Bad', 0)
    pass_percentage = (total_good / (total_good + total_bad)) * 100 if (total_good + total_bad) > 0 else 0
    fail_percentage = (total_bad / (total_good + total_bad)) * 100 if (total_good + total_bad) > 0 else 0

    return percentage_table, pass_percentage, fail_percentage

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
    #04102024
    #bar_plot = sns.barplot(data=result_dataframe, x="bulan", y="jumlah_y", palette=palette)
    bar_plot = sns.barplot(data=result_dataframe, x="bulan", y="jumlah_y", hue="bulan", palette=palette, ax=ax_bar, legend=False)
    #04102024
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
