# Updates to make: limit df to show only the selected tables
# deploy for others to use
# streamlit run app.py --server.maxMessageSize 600

import streamlit as st
import polars as pl
import requests

st.set_page_config(page_title="Oracle Data Dictionary", page_icon=":snake:", layout="wide")

# df = pl.read_parquet('oracle_data_dictionary.parquet')

@st.cache_data
def perform_health_check():
    response = requests.get("http://localhost:8501/healthz")
    return response.status_code == 200

if perform_health_check():
       st.write("App is healthy")
else:
    st.write("App is not healthy")

@st.cache_data
def load_data():
    parquet_file = 'oracle_data_dictionary.parquet'
    return pl.read_parquet(parquet_file)


df = load_data()

# LOAD ASSETS

# HEADER
with st.container():
    st.title("Oracle Data Dictionary")
    st.subheader("Relationship Lookup")
    st.write("This app allows the user to query matching columns between two tables in an Oracle database.")

# DESCRIPTION
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        table_1 = None
        table_1 = left_column.text_input("Please enter the name of your first table:", key = "table_1")
    with right_column:
        table_2 = None
        table_2 = right_column.text_input("Please enter the name of your second table:", key = "table_2")

    st.write("You entered:", table_1, "and", table_2)

    # Only run the following code if table_1 and table_2 contain data
    if table_1 and table_2:
        filtered_df = df.filter(pl.col("RELATIONSHIPS").str.contains(table_1))

        # Filter the resulting dataframe to only include rows where table_2 is in the RELATIONSHIPS column
        filtered_df = filtered_df.filter(pl.col("RELATIONSHIPS").str.contains(table_2))

        # Get the list of matching column names
        matching_columns = set(filtered_df["COLUMN_NAME"].to_list())

        if matching_columns:
            print(f"Matching columns for {table_1} and {table_2}:")
            for column in matching_columns:
                st.write(column)
        else:
            st.write("No matching columns found.")
        
        filtered_df = filtered_df.filter(pl.col("TABLE_NAME").str.contains(table_1) | pl.col("TABLE_NAME").str.contains(table_2))

        # Display the filtered dataframe
        st.header("Filtered Relationships")
        st.dataframe(filtered_df, width=1800, height=500)

# User input
# ! search feature on TABLE_NAME
# ! search feature on COLUMN_NAME
# ! fuzzy matching on COLUMN_NAME
with st.container():
    st.header("Full Data Dictionary")
    st.dataframe(df, width=1800, height=500)
    