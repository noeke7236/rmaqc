import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from streamlit_echarts import st_pyecharts

from config import tahun_2024

from utils import load_data
from utils import calculate_statistics
from utils import calculate_percentage
from utils import display_metrics
from utils import tampilkan_pie_chart
from utils import statistik_barang
from utils import grafik_barang
from utils import grafik_bar_horizontal_count
from utils import grafik_bar_horizontal_sum
from utils import grafik_bar_project

def rma_2024():
    rma = load_data(tahun_2024['url'])
    rma_modified = rma.copy()
    
    st.markdown("# Infografis Tahun "+ tahun_2024['tahun'] +" "+ tahun_2024['icon'])
    st.sidebar.markdown("# "+ tahun_2024['tahun'] + " " + tahun_2024['icon_sidebar'])

    total_items, total_quantity = calculate_statistics(rma_modified)
    good_percentage, fail_percentage, untested_percentage = calculate_percentage(rma_modified, 'Final Status')
    #good_counts, fail_counts, untested_counts, good_percentage, fail_percentage, untested_percentage = calculate_percentage(rma_modified2, 'Final Status')

    display_metrics(total_items, total_quantity, good_percentage, fail_percentage, untested_percentage)
        
    st.divider()
    #st.markdown("""---""")
    
    # PERSENTASE DALAM PROSES QC
    #status_table_data = create_status_table_data(rma_modified2, 'Final Status')
    #status_headers = ['Status', 'Total', 'Persentase(%)']
    #status_subheader = 'Persentase hasil proses QC'
    #status_table_percentage_variable(status_table_data, status_headers, status_subheader)
    
    # PIE CHART PERSENTASE QC
    #display_pie_chart(status_table_data, title='Pie chart Persentase Hasil QC')
    # Prepare data for pie chart
    #labels = ["Pass", "Fail"]
    #values = [good_percentage, fail_percentage]
    #if untested_percentage is not None:
    #    labels.append("Untested")
    #    values.append(untested_percentage)

    # Create a pie chart using pyecharts
    #c = (
    #    Pie()
    #    .add("", [list(z) for z in zip(labels, values)])
    #    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    #    .set_global_opts(opts.InitOpts(width="800px", height="600px"))
    #)

    #st.subheader("Grafik Persentase Status Alat / Barang")

    # Display the pie chart in Streamlit
    #st_pyecharts(c, width="640px", height="480px")
    tampilkan_pie_chart(good_percentage, fail_percentage, untested_percentage)

    # TOTAL BARANG MASUK
    #total_barang_masuk(rma_modified2)
    #tabel_alat_barang(rma_modified2)
             
    # GRAFIK BARANG MASUK
    #grafik_barang_masuk(rma_modified2)
    #grafik_barang(rma_modified2, 'Tgl Masuk [PB06]', 'jumlah_in', 'Grafik barang masuk', "#009EFA")

    # GRAFIK BARANG KELUAR
    #grafik_barang_keluar(rma_modified2)
    #grafik_barang(rma_modified2, 'Tgl Keluar [PB07]', 'jumlah_out', 'Grafik barang keluar', "#FF6347")

    # Menghitung statistik barang masuk dan keluar
    ##data_masuk = statistik_barang(rma_modified, 'Tgl Masuk [PB06]', 'Barang Masuk', "#009EFA")
    ##data_keluar = statistik_barang(rma_modified, 'Tgl Keluar [PB07]', 'Barang Keluar', "#FF6347")

    # Membuat grafik barang masuk dan keluar
    ##bar = grafik_barang(data_masuk, data_keluar)

    # Menampilkan grafik di Streamlit
    ##st.subheader("Grafik Barang Masuk dan Keluar")
    ##st_pyecharts(bar, height="500px")

    #GRAFIK BAR HORIZONTAL COUNT
    #grafik_bar_horizontal_count(rma_modified2)
    grafik_bar_horizontal_count(rma_modified)
    
    #GRAFIK BAR HORIZONTAL SUM
    #grafik_bar_horizontal_sum(rma_modified2)
    grafik_bar_horizontal_sum(rma_modified)
    
    # GRAFIK BAR PROJECT
    #grafik_bar_project(rma_modified, 'Project 2024)
    grafik_bar_project(rma_modified, 'Project '+ tahun_2024['tahun'])
