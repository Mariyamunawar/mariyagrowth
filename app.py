# imports
import streamlit as st
import pandas as pd 
import os
from io import BytesIO


# set up our app
st.set_page_config(page_title="data sweeper",layout='wide')
st.write("data sweeper")
st.write("Transform your files between CSV and Excel format with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("upload you files (CSV or Excel):", type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel (file)  
        else:
            st.error(f"unsupported file type: {file_ext}") 
            continue   
     
        # Display info about the file
        st.write(f"**File name:** {file.name}")
        st.write(f"**file size:**{file.size/1024}")

        # show 5 rows of our df
        st.write("PReview the Head of the Dataframe")
        st.dataframe(df.head())

        # options for data cleaning
        st.subheader("Data cleaning options")
        if st.checkbox(f"clean Data for {file.name}"):
            col1, col2 = st.colums(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"File Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna (df[numeric_cols].mean())  
                    st.write("Missing Values have been Filled!") 


         
                     
        
        
        
        
        
        
        
        
        
        