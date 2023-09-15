
from Paths.paths import LISTINGS_DB_PATH, INFRASTRUCTURE_CSV_PATH


def calculate_score(listing_id, chosen_infra, chosen_intention):
    score = 0
    
    # 2. Infrastructure Weighting
    if chosen_infra != "Any":
        # Use dynamic weights if a specific infrastructure type is chosen
        weights = infra_df[infra_df['infrastructure_type'] == chosen_infra]['dynamic_wheight'].to_dict()
    else:
        # Use standard weights if no specific type is chosen
        weights = infra_df['weights'].to_dict()
    
    for infra_id, weight in weights.items():
        # 3. Distance Penalty
        distance_to_infra = distance_matrix.at[listing_id, str(infra_id)]
        if distance_to_infra <= 500:
            penalty = 1  # No penalty
        elif distance_to_infra <= 1000:
            penalty = 0.7  # 30% penalty
        elif distance_to_infra <= 1500:
            penalty = 0.5  # 50% penalty
        elif distance_to_infra > 2000:
            penalty = 0  # 100% penalty
        
        score += weight * penalty
    
    # 4. Intention Weighting (you'll need to define logic based on your data)
    # Note: This part is kept as it was since the logic depends on your data
    if chosen_intention == "Build & Sell":
        score += listing.property_growth_value  # Placeholder, adjust based on your data structure
    elif chosen_intention == "Rent":
        score += listing.rental_yield  # Placeholder, adjust based on your data structure
    
    return score



# Update the scoring logic function to use the modified calculate_score function
def updated_scoring_logic(listings_df, chosen_zone, chosen_infra, chosen_intention):
    # 1. Initial Filter
    filtered_listings = listings_df
    if chosen_zone != "Any":
        filtered_listings = filtered_listings[filtered_listings.zone == chosen_zone]
    
    # 5. Calculate Final Score
    filtered_listings['score'] = filtered_listings['index'].apply(calculate_score, args=(chosen_infra, chosen_intention))
    
    # 6. Sort Listings
    sorted_listings = filtered_listings.sort_values(by='score', ascending=False)
    
    return sorted_listings

# Return the updated function for further use
updated_scoring_logic





