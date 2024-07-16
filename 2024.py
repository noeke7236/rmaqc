def rma_2024():
    st.markdown("# Infografis Tahun 2024")
    st.sidebar.markdown("# 2024 :bar_chart:")

    st.markdown("""---""")

    # TOTAL BARANG MASUK
    # Calculate statistics
    row_count2, total_qty2 = calculate_statistics(rma_modified2)
    tabel_barang2 = pd.DataFrame({'Kategori': ['Total Barang', 'Total Kuantitas'], 'Nilai': [row_count2, total_qty2]})
    st.subheader('Total Alat/Barang')
    st.markdown(tabel_barang2.style.hide(axis="index").to_html(), unsafe_allow_html=True)
