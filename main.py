import streamlit as st
from functions.cleaning import show_cleaning_page
from functions.summary import show_summary_page
from functions.visualization import show_visualization_page

st.set_page_config(page_title="Data Cleaner and Visualizer",layout="wide")

Menu = st.sidebar.selectbox("Menu",("Data Summarizer","Data Cleaner","Data Visualizer"))
title = st.title("Data Summarizer | Cleaner | Visualizer")

upload_files = st.file_uploader("Upload xlsx and csv file", type=["xlsx", "csv"], accept_multiple_files=True)

if Menu == "Data Summarizer":
    show_summary_page(upload_files)
elif Menu == "Data Cleaner":
    show_cleaning_page(upload_files)
elif Menu == "Data Visualizer":
    show_visualization_page(upload_files)
else:
    st.error("Incorrect option!")



st.markdown("---")
st.markdown("#### Developed by Rao Hamza Tariq.")