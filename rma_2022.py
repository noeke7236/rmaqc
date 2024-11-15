# rma_2022

import streamlit as st
import pandas as pd

from streamlit_echarts import st_pyecharts

from config import tahun_2022
from config import mylist

from utils import load_data
from utils import normalize_columns
from utils import calculate_statistics
from utils import calculate_percentage
from utils import display_metrics
#from utils import tabel_alat_barang
from utils import tampilkan_pie_chart
from utils import statistik_barang
from utils import grafik_barang

#url3 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQPxyl1P5AOFTBbTNR2f1TH3jP69HJigz2nnixuT2Ft3E67jeQFerdFoD5heO9YSY-Zi_H7TjHrTu3x/pub?output=xlsx'
#rma3 = load_data(url3)

#mylist = ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 'Tgl Masuk [PB06]', 'Tgl Keluar [PB07]', 'Final Status', 'Project']

def rma_2022():
    rma = load_data(tahun_2022['url'])
    rma_modified = rma.copy()
    rma_modified = normalize_columns(rma_modified, mylist)

    st.markdown("# Infografis Tahun "+ tahun_2022['tahun'] +" "+ tahun_2022['icon'])
    st.sidebar.markdown("# "+ tahun_2022['tahun'] +" "+ tahun_2022['icon_sidebar'])
    
    total_items, total_quantity = calculate_statistics(rma_modified)
    good_percentage, fail_percentage, untested_percentage = calculate_percentage(rma_modified, 'Final Status')
    
    display_metrics(total_items, total_quantity, good_percentage, fail_percentage, untested_percentage)
    
    st.divider()

    # TOTAL BARANG MASUK
    #tabel_alat_barang(rma_modified)

    # PIE CHART PERSENTASE QC
    tampilkan_pie_chart(good_percentage, fail_percentage, untested_percentage)

    # GRAFIK BARANG MASUK & BARANG KELUAR
    data_masuk = statistik_barang(rma_modified, 'Tgl Masuk [PB06]', 'Barang Masuk', "#009EFA")
    data_keluar = statistik_barang(rma_modified, 'Tgl Keluar [PB07]', 'Barang Keluar', "#FF6347")
    bar = grafik_barang(data_masuk, data_keluar)
    st.subheader("Grafik Barang Masuk dan Keluar")
    st_pyecharts(bar, height="500px")
