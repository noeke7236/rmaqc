# rma_2022

import streamlit as st
import pandas as pd

from utils import load_data
from utils import normalize_columns
from utils import calculate_statistics
from utils import calculate_percentage
from utils import display_metrics

url3 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQPxyl1P5AOFTBbTNR2f1TH3jP69HJigz2nnixuT2Ft3E67jeQFerdFoD5heO9YSY-Zi_H7TjHrTu3x/pub?output=xlsx'
rma3 = load_data(url3)

mylist = ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 'Tgl Masuk [PB06]', 'Tgl Keluar [PB07]', 'Final Status', 'Project']

def rma_2022():
    #st.markdown('<span style="font-size: 24px;">Infografis Tahun 2022</span>', unsafe_allow_html=True)
    st.markdown("# Infografis Tahun 2022 :tiger:")
    st.sidebar.markdown("# 2022 :tiger2:")

    rma_modified3 = rma3.copy()
    rma_modified3 = normalize_columns(rma_modified3, mylist)

    total_items, total_quantity = calculate_statistics(rma_modified3)

    #percentage_table, rma2022_pass_percentage, rma2022_fail_percentage = calculate_percentage(rma_modified3)
    #rma2022_counts, rma2022_percentage, #rma2022_pass_percentage,rma2022_fail_percentage = #calculate_percentage(rma_modified3)

    #col1, col2, col3, col4 = st.columns(4)
    #col1.metric("Total Items", total_items2)
    #col2.metric("Total Quantity", total_quantity2)
    #col3.metric("Pass :heavy_check_mark:", f"{rma2022_pass_percentage:.1f}%")
    #col4.metric("Fail :x:", f"{rma2022_fail_percentage:.1f}%")

    # Calculate the percentages
    good_percentage, fail_percentage, untested_percentage = calculate_percentage(rma_modified3, 'Final Status')

    display_metrics(total_items, total_quantity, good_percentage, fail_percentage, untested_percentage)

    st.divider()
