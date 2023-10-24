# Update Python Path at runtime
import sys
sys.path.append('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main_App')


import streamlit as st
import pandas as pd
import sqlite3
from Scoring.scoring_logic import updated_scoring_logic
from Paths.paths import LISTINGS_DB_PATH
from Paths.connect_db import create_connection



# IF THE PATHS ARE NOT WORKING, RUN THIS!

# import os
# print(os.getcwd())

# import os

# # Print the current working directory
# print("Current Working Directory:", os.getcwd())

# # Change the working directory
# os.chdir('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main_App')

# # Print the current working directory again to confirm the change
# print("New Working Directory:", os.getcwd())


# Initialize listing dataframe
listings_df = pd.DataFrame()


conn = create_connection()
if conn is None:
    st.error("Unable to establish a connection to the database.")
else:
    listings_df = pd.read_sql_query("SELECT * FROM listings", conn)


# User Input
investment_amount = st.number_input("How much do you intend to invest?", min_value=0.0, step=100.0)

zones = ["Zone 1", "Zone 2", "Zone 3", "Any"]
chosen_zone = st.selectbox("Select a zone:", zones)

intentions = ["Build & Sell", "Rent", "Any"]
chosen_intention = st.selectbox("What is your intention?", intentions)

infra_options = ["Infrastructure 1", "Infrastructure 2", "Infrastructure 3", "Any"]
chosen_infra = st.selectbox("Which infrastructure is most important to you?", infra_options)


# Filter Listings
filtered_listings = listings_df
if chosen_zone != "Any":
    filtered_listings = filtered_listings[filtered_listings['zone'] == chosen_zone]

# Initialize to an empty DataFrame
sorted_listings = pd.DataFrame()  

#Apply scoring logic
try:
    sorted_listings = updated_scoring_logic(filtered_listings, chosen_zone, chosen_infra, chosen_intention)
except Exception as e:
    st.error(f"An error occurred while applying scoring logic: {e}")
    sorted_listings = pd.DataFrame()


if not sorted_listings.empty:
    st.write(sorted_listings)
else:
    st.write("No listings to display.")



