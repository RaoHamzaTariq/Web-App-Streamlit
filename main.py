import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

st.title("Data Cleaning and Visualization")
st.write("Clean the dataset and Visualize the dataset with some findings.")

upload_files = st.file_uploader("Upload xlsx and csv file", type=["xlsx", "csv"], accept_multiple_files=True)

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

        st.header(f"File Name: {file.name}")
        st.write(f"File Size: {file.size / 1024:.2f} KB")

        rows, columns = dataset.shape
        st.write(f"The number of rows and columns are {rows} and {columns}")

        st.write("Preview of First 10 rows of Dataset")
        st.dataframe(dataset.head(10))

        st.write("Preview of Last 10 rows of Dataset")
        st.dataframe(dataset.tail(10))

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Data Cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Remove Duplicate Rows"):
                    dataset.drop_duplicates(inplace=True)
                    st.write("Duplicate Rows Removed")

            with col2:
                if st.button("Handle Missing Values"):
                    numerical_columns = dataset.select_dtypes(include=np.number).columns
                    dataset[numerical_columns] = dataset[numerical_columns].fillna(dataset[numerical_columns].mean())
                    st.write("Missing values filled successfully!")

        st.subheader("Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose Columns for {file.name}", dataset.columns, default=dataset.columns)
        dataset = dataset[selected_columns]

        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(dataset.select_dtypes(include=np.number).iloc[:, :2])

        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "EXCEL"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                dataset.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "EXCEL":
                dataset.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  

            st.download_button(label=f"Download {file.name} as {conversion_type}",
                   data=buffer.getvalue(),
                   file_name=file_name, 
                   mime=mime_type)

            
    st.success("All files processed!")


st.markdown("---")
st.markdown("#### Developed by Rao Hamza Tariq.")