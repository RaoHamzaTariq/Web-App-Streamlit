import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

def show_cleaning_page(upload_files):
    st.header("Data Cleaner")
    st.write("This helps you to clean the dataset.")


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

            with st.expander(f"Cleaning for {file.name}"):

                st.subheader("Data Cleaning Options")
                
                if st.button("Remove Duplicated values",key=f"duplicate_{file.name}"):
                    duplicated_values = dataset.duplicated().sum()
                
                    if duplicated_values:
                        dataset = dataset.drop_duplicates()
                        st.write(f"Removed {duplicated_values} duplicate rows.")
                    else:
                        st.write("No duplicates found.")
                
                if st.button("Handle Missing Values",key=f"missing_{file.name}"):
                    if dataset.isna().sum().sum() == 0:
                        missing_percent = dataset.isnull().mean() * 100
                        dataset = dataset.drop(columns=missing_percent[missing_percent > 40].index)

                        # Fill missing values
                        for column in dataset.columns:
                            if dataset[column].isnull().sum() > 0:
                                if dataset[column].dtype == "object":
                                    dataset[column] = dataset[column].fillna(dataset[column].mode()[0])  
                                else:
                                    dataset[column] = dataset[column].fillna(dataset[column].median()) 

                        st.write("Missing values handled successfully!")
                    else:
                        st.write("No missing data found")



                st.subheader("Conversion Options")
                conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "EXCEL"], key=file.name)

                if st.button(f"Convert {file.name}",key=f"Convert_{file.name}"):
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


