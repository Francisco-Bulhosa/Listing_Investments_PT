
from Paths.paths import LISTINGS_DB_PATH, INFRASTRUCTURE_CSV_PATH
from Paths import connect_db
import pandas as pd

class metrics:

    
    # Load the infrastructure data
    infra_df = pd.read_csv(INFRASTRUCTURE_CSV_PATH)

    # Create datafram for Distance Matrix
    distance_matrix = pd.DataFrame()

    conn = create_connection()
    if conn is None:
        st.error("Unable to establish a connection to the database.")
    else:
        distance_matrix = pd.read_sql_query("SELECT * FROM distance_matrix", conn)
        

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





def calculate_cash_flow(rental_income, expenses):
    return rental_income - expenses

def one_percent_rule(purchase_price):
    return purchase_price * 0.01

def calculate_cap_rate(NOI, purchase_price):
    return (NOI / purchase_price) * 100

def calculate_ROI(net_profit, initial_investment):
    return (net_profit / initial_investment) * 100

def calculate_GRM(purchase_price, annual_rental_income):
    return purchase_price / annual_rental_income
