

def base_rental_income(num_rooms):
    if num_rooms == 1:
        return 600
    elif num_rooms == 2:
        return 1100
    elif num_rooms == 3:
        return 1500
    elif num_rooms == 4:
        return 2000
    elif num_rooms == 5:
        return 2500
    elif num_rooms == 6:
        return 2800
    else:
        return 2800 + (300 * (num_rooms - 6))


def adjust_rental_income_for_infrastructure(base_rental_income, listing_id):
    adjustment_factor = 1.0  # Start with no adjustment
    
    for infra_idx, infra_row in infra_df.iterrows():
        distance = distance_matrix.at[listing_id, infra_idx]
        
        # Define thresholds for distance - these can be tweaked based on your requirements
        if distance < 500:
            adjustment = infra_row['weights'] * 0.15  # 15% adjustment per weight for very close infrastructures
        elif distance < 1000:
            adjustment = infra_row['weights'] * 0.075  # 7.5% adjustment per weight for moderately close infrastructures
         elif distance < 1500:
            adjustment = infra_row['weights'] * 0.03  # 3% adjustment per weight for moderately close infrastructures
        else:
            adjustment = 0  # No adjustment for far away infrastructures
        
        adjustment_factor += adjustment

    # Cap the adjustment factor to avoid too high rentals
    adjustment_factor = min(adjustment_factor, 1.5)  # For example, cap at 50% increase

    return base_rental * adjustment_factor