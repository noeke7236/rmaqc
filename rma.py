# Contents of ~/rmaqc/rma.py
import streamlit as st

st.set_page_config(
    page_title="RMA&QC",
    page_icon=":watermelon:",
)

def rma_qc():
    st.markdown("# RMA QC 🎈")
    st.sidebar.markdown("# RMA QC 🎈")

def rma_2023():
    st.markdown("# 2023 :tulip:")
    st.sidebar.markdown("# 2023 :tulip:")

image_url = "https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg"
image = plt.imread(image_url)
st.sidebar.image(image, caption='Your Image Caption', use_column_width=True)
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
