import numpy as np
import pandas as pd
import datetime

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

def get_week_dates_from_week_number():
    # Mendapatkan tanggal sekarang
    today = datetime.date.today()

    # Mendapatkan nomor urut pekan dari tanggal sekarang
    week_number = today.isocalendar()[1]

    # Mendapatkan tanggal awal dari pekan yang bersangkutan
    start_of_week = today - datetime.timedelta(days=today.weekday())

    # Mendapatkan tanggal akhir dari pekan yang bersangkutan
    end_of_week = start_of_week + datetime.timedelta(days=6)

    return week_number, start_of_week, end_of_week

# Memanggil fungsi dan mendapatkan hasil
# week_number, start_date, end_date = get_week_dates_from_week_number()

# first_date = start_date.strftime("%d/%m/%Y")
# last_date = end_date.strftime("%d/%m/%Y")
# Menampilkan hasil
# print(f"Week Number: {week_number}")
# print(f"Start Date: {first_date}")
# print(f"End Date: {last_date}")
