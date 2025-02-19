import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from streamlit_echarts import st_pyecharts

from config import mylist
from config import columns_to_drop

from config import tahun_2023

from utils import load_data
from utils import calculate_statistics
from utils import calculate_percentage, calculate_percentage2
from utils import display_metrics
from utils import drop_columns
from utils import normalize_columns

from utils import tampilkan_pie_chart, tampilkan_pie_chart1
from utils import statistik_barang
from utils import grafik_barang
from utils import grafik_bar_horizontal_count
from utils import grafik_bar_horizontal_sum
from utils import grafik_bar_project

def rma_2023():
    tahun = int(tahun_2023['tahun'])
    
    st.markdown("# Infografis Tahun "+ str(tahun_2023['tahun']) +" "+ tahun_2023['icon'])
    st.sidebar.markdown("# "+ str(tahun_2023['tahun']) + " " + tahun_2023['icon_sidebar'])
    #rma = load_data_new(tahun_2023['tipe'], tahun_2023['url'])
    rma = load_data(tahun_2023['tipe'], tahun_2023['url'])
    
    rma_modified = rma.copy()
    rma_modified = drop_columns(rma_modified, columns_to_drop)
    rma_modified = normalize_columns(rma_modified, mylist)
   	
    total_items, total_quantity = calculate_statistics(rma_modified)
    good_percentage, fail_percentage, untested_percentage = calculate_percentage(rma_modified, 'Final Status')
    
    L0_counts, L1_counts, L2_counts, L3_counts, L0_percentage, L1_percentage, L2_percentage, L3_percentage = calculate_percentage2(rma_modified, 'RMA Level')
    
    display_metrics(total_items, total_quantity, good_percentage, fail_percentage, untested_percentage)
    
    st.divider()
    
    tampilkan_pie_chart(good_percentage, fail_percentage, untested_percentage)

    tampilkan_pie_chart1(L0_percentage, L1_percentage, L2_percentage, L3_percentage)

    # Menghitung statistik barang masuk dan keluar
    data_masuk = statistik_barang(rma_modified, 'Tgl Masuk [PB06]', 'Barang Masuk', "#009EFA", tahun)
    data_keluar = statistik_barang(rma_modified, 'Tgl Keluar [PB07]', 'Barang Keluar', "#FF6347", tahun)

    # Membuat grafik barang masuk dan keluar
    bar = grafik_barang(data_masuk, data_keluar)

    # Menampilkan grafik di Streamlit
    st.subheader("Grafik Barang Masuk dan Keluar")
    st_pyecharts(bar, height="500px")

    #GRAFIK BAR HORIZONTAL COUNT
    grafik_bar_horizontal_count(rma_modified)
    
    #GRAFIK BAR HORIZONTAL SUM
    grafik_bar_horizontal_sum(rma_modified)
    
    # GRAFIK BAR PROJECT
    grafik_bar_project(rma_modified)
