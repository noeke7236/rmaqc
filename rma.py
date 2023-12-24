# Contents of ~/rmaqc/rma.py
import streamlit as st
import matplotlib as plt
from wordcloud import WordCloud

st.set_page_config(
    page_title="RMA&QC",
    page_icon=":watermelon:",
)

wc = WordCloud().fit_words({"R": 2, "M": 2, "A": 2})
st.sidebar.image(wc.to_array(),use_column_width=True)

def rma_qc():
    st.markdown("# RMA QC 🎈")
    st.sidebar.markdown("# RMA QC 🎈")
    st.header('Alur Kerja', divider='rainbow')
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/rma_flowchart.png')
 
def rma_2023():
    st.markdown("# 2023 :tulip:")
    st.sidebar.markdown("# 2023 :tulip:")

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
