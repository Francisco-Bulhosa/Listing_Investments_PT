import streamlit as st
import pandas as pd
import sqlite3
import os

# Define the path to your SQLite database file
db_path = 'C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main_App\\Scraper\\listings.db'

# Check if the file exists
if os.path.exists(db_path) and os.access(db_path, os.R_OK):
    st.write("Database file found and is readable.")

    # Establish a connection to the SQLite database
    conn = sqlite3.connect(db_path)

    # Load data from the "listings" table into a Pandas DataFrame
    query = "SELECT * FROM listings"
    listings_df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Display the DataFrame in Streamlit
    st.write(listings_df)

else:
    st.error("Either the file is missing or not readable. Please check the file path and permissions.")
