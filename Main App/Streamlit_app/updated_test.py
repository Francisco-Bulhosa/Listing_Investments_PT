import streamlit as st
import pa

# Assuming listings_df is loaded somewhere in your app, replace with actual dataframe name
sorted_listings = updated_scoring_logic(listings_df, chosen_zone, chosen_infra, chosen_intention)
st.write(sorted_listings)

ndas as pd

import sqlite3


import pandas as pd

# Load the infrastructure data
infra_df = pd.read_csv("/mnt/data/Infrastructure.csv")

def scoring_logic(listings_df, chosen_zone, chosen_infra, chosen_intention):

    from Paths.paths import LISTINGS_DB_PATH, INFRASTRUCTURE_CSV_PATH
    
    
    def calculate_score(listing, chosen_infra, chosen_intention):
        score = 0
    
        # 2. Infrastructure Weighting
        if chosen_infra != "Any":
            # Give higher weight to chosen_infra
            weight = infra_weights[chosen_infra] * 1.5  # 1.5 is an arbitrary multiplier
        else:
            weight = infra_weights[chosen_infra]
    
        # 3. Distance Penalty
        distance_to_infra = distance_matrix.loc[listing.id, chosen_infra]
        if distance_to_infra <= 500:
            penalty = 1  # No penalty
        elif distance_to_infra <= 1000:
            penalty = 0.7  # 30% penalty
        elif distance_to_infra <= 1500:
            penalty = 0.5  # 50% penalty
        elif distance_to_infra > 2000:
            penalty = 0 # 100% penalty
    
        weight *= penalty
    
        score += weight
    
        # 4. Intention Weighting (you'll need to define logic based on your data)
        if chosen_intention == "Build & Sell":
            score += listing.property_growth_value
        elif chosen_intention == "Rent":
            score += listing.rental_yield
    
        return score
    
    
    
    
    # 1. Initial Filter
    filtered_listings = listings_df
    if chosen_zone != "Any":
        filtered_listings = filtered_listings[filtered_listings.zone == chosen_zone]
    
    # 5. Calculate Final Score
    filtered_listings['score'] = filtered_listings.apply(calculate_score, args=(chosen_infra, chosen_intention), axis=1)
    
    # 6. Sort Listings
    sorted_listings = filtered_listings.sort_values(by='score', ascending=False)
    
    


    return sorted_listings



# Connect to the SQLite database
conn = sqlite3.connect("/mnt/data/listings.db")
# Load infrastructure data
infra_df = pd.read_csv("/mnt/data/Infrastructure.csv")

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

# Apply Weights and Penalties
# Fetch listings
listings = get_listings_from_db()  # Fetched from the get_listings.py 

# Calculate scores for each listing
scores = []
for listing in listings:
    score = calculate_score(listing, chosen_infra, chosen_intention)
    scores.append(score)


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