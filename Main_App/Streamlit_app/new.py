# Update Python Path at runtime
import sys
sys.path.append('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main_App')


import streamlit as st
import pandas as pd
import sqlite3
from Scoring.metrics import *
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


# Connect to the SQLite database for listings
conn = sqlite3.connect(LISTINGS_DB_PATH)
listings_df = pd.read_sql_query("SELECT * FROM listings", conn)


# Load infrastructure data
infra_df = pd.read_csv(INFRASTRUCTURE_CSV_PATH)

# Title of the app
st.title("Real Estate Investment Advisor")

# 1. User Input
investment_amount = st.number_input("How much do you intend to invest?", min_value=0.0, step=100.0)
zones = ["Costa da Caparica", "Caparica e Trafaria", "Charneca de Caparica e Sobreda", "Laranjeiro e Feijó",
"Almada, Cova da Piedade, Pragal e Cacilhas", "Any"]  # Replace your zones
chosen_zone = st.selectbox("Select a zone:", zones)

intentions = ["Build & Sell", "Rent", "Any"]
chosen_intention = st.selectbox("What is your intention?", intentions)

infra_options = ["High Relevance (Bridge, Fórum)", "Hospital", "Metro & Train Station", "Beaches", "University", "Any"]
chosen_infra = st.selectbox("Which infrastructure is most important to you?", infra_options)


# Filter Listings Based on User Input
filtered_listings = listings_df
if chosen_zone != "Any":
    filtered_listings = filtered_listings[filtered_listings.zone == chosen_zone]

# 3. Apply Weights and Penalties
# Note: The function updated_scoring_logic should take care of calculating scores, applying weights and penalties
try:
    sorted_listings = updated_scoring_logic(filtered_listings, chosen_zone, chosen_infra, chosen_intention, investment_amount)
except Exception as e:
    st.error(f"An error occurred while applying scoring logic: {str(e)}")
    sorted_listings = pd.DataFrame()

# 4. Show Results
if not sorted_listings.empty:
    st.write("Top Results:")
    st.write(sorted_listings.head(10))  # Displaying top 10 results
else:
    st.write("No listings to display.")


st.write("Investment Amount:", investment_amount)
st.write("Chosen Zone:", chosen_zone)
st.write("Chosen Intention:", chosen_intention)
st.write("Chosen Infrastructure:", chosen_infra)


st.write("Filtered Listings:")
st.write(filtered_listings)


