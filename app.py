# Imports
import streamlit as st 
import pandas as pd 
import os 
from io import BytesIO 


# Set up our App 
st.set_page_config(page_title="📀Data sweeper", layout='wide') 
st.title("📀Data sweeper") 
st.write("transfrom your files between CSV and Excel formats with built-in data cleaning and visualization!") 

uploaded_files = st.file_uploader("uplod you files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True) 

if uploaded_files: 
    for files in uploaded_files: 
        file_exy = os.path.splitext(file.name)[-1].lower() 


        if file_ext == ".csv": 
            df = pd.read_csv(file)
        elif file_ext == ".xlsx": 
            df = pd.read_excel(file) 
        else:
            st.error(f"unsupported file type: {file-ext}") 
            continue 

        # Display info about the file 
        st.write(f"**file name:** {file.name}") 
        st.write(f"**file size:** {file.size/1024}") 

        # show 5 rows of our df 
        st.write("🔍preview the Head of tha Dataframe") 
        st.dataframe(df.head()) 

        # Options for data cleaning 
        st.subheader("🛠️Data Cleaning Options") 
        if st.checkbox(f"Clean Data for {file.name}"): 
            col1, col2 = st.columns(2) 

            with col1: 
                if st.button(f"Remove Duplicat from {file.name}"): 
                    df.drop_duplicates(inplace=True) 
                    st.write("Duplicates Removed!") 

            with col2: 
                if st.button(f"fill Missing Values for {file.name}"): 
                    numeric_cols = df.select_dtypes(include=['number']).columns 
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean()) 
                    st.write("Missing Values have Filled!") 


            # Choose Specific Columns to keep or convert 
            st.subheader("🎯Select Columns to convert") 
            columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns) 
            df = df[columns] 


            # Creats Some Visualizations 
            st.subheader("📊 Data visualization") 
            if st. checkbox(f"Show visualization for {file.name}"): 
                st.bar_chart(df.select_dtypes(include='nimber').iloc[:,:2]) 


            # Convert the file -> CSV to Excel 
            st.subheader("🔄Conversion Options") 
            conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"], key=file.name) 
            if st.button(f"convert {file.name}"): 
                buffer = BytesIO()
                if conversion_type == "CSV": 
                    df.to_csv(buffer,index=False) 
                    file_name = file.name.replace(file_ext,".csv") 
                    mime_type = "text/csv" 

                elif conversion_type == "Excel":
                    df.to_excel(buffer,index=False) 
                    file_name = file.name.replace(file_ext,".xlsx")
                    mime_type = "application/vnd.Openxmlformats-officedocument.spreadsheetml.sheet" 
                buffer.seek(0) 


                # Download Button 
                st.download_button(
                    label=f"⬇️ Download {file.name} as {conversion_type}", 
                    data=buffer,
                    file_name=file_name, 
                    mime=mime_type
                ) 

st.success("🎉 All files processed!")
st.write("**created by mariya munawar**")
        