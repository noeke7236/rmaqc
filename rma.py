# Contents of ~/rmaqc/rma.py
import streamlit as st

def rma_qc():
    st.markdown("# RMA QC 🎈")
    st.sidebar.markdown("# RMA QC 🎈")

def rma_2023():
    st.markdown("# 2023 :watermelon:")
    st.sidebar.markdown("# 2023 :watermelon:")

#def page3():
#    st.markdown("# Page 3 🎉")
#    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "RMA QC": rma_qc,
    "2023": rma_2023,
    #"Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
