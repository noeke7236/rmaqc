import streamlit as st
import streamlit_scrollable_textbox as stx
from annotated_text import annotated_text, annotation

def rma_qc():
    st.markdown("# QC & RMA ")
    st.sidebar.markdown("# QC & RMA ")

    annotated_text(
        ("\"", "", "#fff"),  # Tanda petik pembuka
        ("Creative", "", "#ffa500"),
        " minds drive innovation, ",
        ("Proactive", "", "#faa"),
        " actions shape the future, ",
        ("Trustworthy", "", "#afa"),
        " values build strong relationships, and ",
        ("Unity", "", "#8ef"),
        " brings lasting success.",
        ("\"", "", "#fff")   # Tanda petik penutup
    )
    
    st.header('Deskripsi', divider='rainbow')
    with open('deskripsi.txt', 'r') as file:
        deskripsi = file.read()
    stx.scrollableTextbox(deskripsi)

    st.header('Alur Kerja', divider='rainbow')
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/rma_flowchart.png')
    st.text("")
    st.text("")
    st.header('Knowledge Base', divider='rainbow')
    url_link = "http://kb.mindotama.co.id/dokuwiki/doku.php?id=start"
    st.write("QC & RMA Knowledge Base [link](%s)" % url_link)
    #st.markdown("check out this [link](%s)" % url)
    st.image('https://raw.githubusercontent.com/noeke7236/rmaqc/main/images/webkbmindotama.png')
