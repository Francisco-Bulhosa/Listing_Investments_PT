# Update Python Path at runtime
import sys
sys.path.append('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main_App')

from Paths.paths import LISTINGS_DB_PATH, INFRASTRUCTURE_CSV_PATH
from Paths.connect_db import create_connection
from Scoring.metrics import *
import pandas as pd
import streamlit as st


    # Load the infrastructure data
infra_df = pd.read_csv(INFRASTRUCTURE_CSV_PATH)

# Create a dictionary of infrastructure weights
infra_weights = infra_df.set_index('infrastructure_type')['weights'].to_dict()


# Create datafram for Distance Matrix
distance_matrix = pd.DataFrame()

conn = create_connection()
if conn is None:
    st.error("Unable to establish a connection to the database.")
else:
    distance_matrix = pd.read_sql_query("SELECT * FROM distance_matrix", conn)




def updated_scoring_logic(listings_df, chosen_zone, chosen_infra, chosen_intention, investment_amount):

            
        
    def calculate_score(listing, chosen_infra, chosen_intention):
        score = 0

        # Print input values
        st.write("Listing:", listing)
        st.write("Chosen Infrastructure:", chosen_infra)
        st.write("Chosen Intention:", chosen_intention)

        try:
                
            # Use user inputs in calculations
            if chosen_intention == "Build & Sell":
                # Example: Prefer listings with higher property growth value
                score += listing['property_growth_value']
                
            elif chosen_intention == "Rent":
                # Example: Calculate adjusted rental income
                num_rooms = listing['num_rooms']
                base_rental = metrics.base_rental_income(num_rooms)
                adjusted_rental = metrics.adjust_rental_income_for_infrastructure(base_rental, listing.id, infra_df, distance_matrix)
                score += adjusted_rental


            if chosen_infra != "Any":
                # If a specific infrastructure is chosen, use its weight
                weight = infra_weights.get(chosen_infra, 1) * 1.5  # Using 1 as default weight if not found
                
                # Calculate the distance penalty based on the distance to the chosen infrastructure
                distance_to_infra = distance_matrix.loc[listing.id, chosen_infra]
                if distance_to_infra <= 500:
                    penalty = 1  # No penalty
                elif distance_to_infra <= 1000:
                    penalty = 0.7  # 30% penalty
                elif distance_to_infra <= 1500:
                    penalty = 0.5  # 50% penalty
                elif distance_to_infra > 2000:
                    penalty = 0  # 100% penalty
                
                # Apply the penalty to the weight
                weight *= penalty
                
                # Add the infrastructure score to the total score
                score += weight
            else:
                # If "Any" is selected, ignore weights
                weight = 1
                penalty = 1  # No penalty
                score += weight * penalty  # This will just add 1 to the score
            
            # Add intention-based scoring
            # (You need to define this part based on your data and requirements)
            if chosen_intention == "Build & Sell":
                score += listing.property_growth_value
            elif chosen_intention == "Rent":
                score += listing.rental_yield

            if not isinstance(score, (int, float)):
                print(f"Non-scalar value detected: {score}")
                print(f"Listing: {listing}")
                raise ValueError("Score is not a scalar value.")
        
        except Exception as e:
            print(f"Error calculating score for listing: {listing}")
            print(f"Exception: {e}")
            score = 0  # You might want to handle this differently

        # Print calculated score
        st.write("Calculated Score:", score)

        return score
    
    
    # 1. Initial Filter
    filtered_listings = listings_df
    if chosen_zone != "Any":
        filtered_listings = filtered_listings[filtered_listings.zone == chosen_zone]

    filtered_listings['score'] = filtered_listings.apply(calculate_score, args=(chosen_infra, chosen_intention), axis=1)
    
    sorted_listings = filtered_listings.sort_values(by='score', ascending=False)


    return sorted_listings



