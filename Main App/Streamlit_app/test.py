import streamlit as st
import pandas as pd
from Scoring.scoring_logic import calculate_score
import sqlite3


# Connect to the SQLite database
conn = sqlite3.connect('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main App\\Scraper\\listings.db')
# Load infrastructure data
infra_df = pd.read_csv('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main App\\Infrastructue_data\\Infrastructure.csv')

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

#Apply Weights and Penalties
# Calculate the score for each listing using the calculate_score function
filtered_listings['score'] = filtered_listings.apply(
    lambda row: calculate_score(row, chosen_infra, chosen_intention), axis=1)

# Sort Listings Based on Score
sorted_listings = filtered_listings.sort_values(by='score', ascending=False)



# Placeholder for top 10 results and map
results_placeholder = st.empty()
map_placeholder = st.empty()

if st.button('Show Results'):
    # Placeholder for demonstration, replace with actual top 10 results
    results_placeholder.write("Top 10 Results will be displayed here")
    map_placeholder.map(listings_df.head(10))  # Displaying first 10 rows as an example

# 4. Reset Button
if st.button('Reset'):
    # Clear the input fields
    st.experimental_rerun()