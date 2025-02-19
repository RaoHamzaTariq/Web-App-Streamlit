import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os
from io import BytesIO

def show_visualization_page(upload_files):
    st.header("Data Visualizer")
    st.write("This helps you to visualize the dataset.")

    if upload_files:
        for file in upload_files:
            file_extension = os.path.splitext(file.name)[-1].lower()

            if file_extension == ".csv":
                dataset = pd.read_csv(file)
            elif file_extension == ".xlsx":
                dataset = pd.read_excel(file)
            else:
                st.error("Invalid file! You can only upload files with '.csv' and '.xlsx'")
                continue

            with st.expander(f"Visualization for {file.name}"):
                column1 = st.selectbox("Column 1",(dataset.columns.tolist()),key=f"column1_for_{file.name}")
                column2 = st.selectbox("Column 2",(dataset.columns.tolist()),key=f"column2_for_{file.name}")
                chart_type = st.selectbox("Chart Type",("Bar Chart","Line Chart","Scatter Plot"),key=f"chart_type_{file.name}")
                if chart_type == "Bar Chart":
                    st.bar_chart(data=dataset,x=column1,y=column2)
                elif chart_type == "Line Chart":
                    st.line_chart(data=dataset,x=column1,y=column2)
                elif chart_type == "Scatter Plot":
                    st.scatter_chart(data=dataset,x=column1,y=column2)
                else:
                    st.error("Invalid Chart Type!")
