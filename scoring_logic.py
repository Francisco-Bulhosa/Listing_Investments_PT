from Paths.paths import LISTINGS_DB_PATH, INFRASTRUCTURE_CSV_PATH
from Paths.connect_db import create_connection
import pandas as pd

# Load the infrastructure data
infra_df = INFRASTRUCTURE_CSV_PATH

def updated_scoring_logic(listings_df, chosen_zone, chosen_infra, chosen_intention):
    
    def scoring_logic(listings_df, chosen_zone, chosen_infra, chosen_intention):
        
        
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


    return sorted_listings
