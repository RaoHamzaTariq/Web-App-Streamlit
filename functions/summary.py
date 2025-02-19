import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

def show_summary_page(upload_files):
    st.header("Data Summarizer")
    st.write("This helps you to check the summary of the dataset.")

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

            with st.expander(f"Summary for {file.name}"):
                st.header(f"File Name: {file.name}")
                st.write(f"File Size: {file.size / 1024:.2f} KB")

                rows, columns = dataset.shape
                st.write(f"The number of rows and columns are {rows} and {columns}")

                st.subheader("Preview of First 10 rows of Dataset")
                st.dataframe(dataset.head(10))

                st.subheader("Preview of Last 10 rows of Dataset")
                st.dataframe(dataset.tail(10))

                st.subheader("Columns of Dataset")
                columns = dataset.columns.tolist()
                st.write(" , ".join(columns))

                if "show_dtypes" not in st.session_state:
                    st.session_state.show_dtypes = False

                if st.button(f"Show DataTypes", key=f"datatype_of_{file.name}"):
                    st.subheader("DataTypes of Columns")
                    for col in columns:
                        st.write(f"{col}: {dataset[col].dtype}")

                if st.button(f"Missing Values of Dataset",key=f"missing_{file.name}"):
                    missing_values = dataset.isnull().sum()
                    st.write(missing_values)

                
                numeric_cols = dataset.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    st.subheader("Summary of Numerical Data")
                    st.write(dataset[numeric_cols].describe())
                    st.subheader("Correlation of Numerical Data")
                    st.write(dataset[numeric_cols].corr())
                else:
                    st.write("No numeric columns found.")

               
                