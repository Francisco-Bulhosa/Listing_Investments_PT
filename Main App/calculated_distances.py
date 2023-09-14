import math
import pandas as pd
import sqlite3


# Connect to the SQLite database
conn = sqlite3.connect('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main App\\Scraper\\listings.db')

# Load real estate listings data
listings_df = pd.read_sql_query("SELECT * FROM listings", conn)

# Load infrastructure data
infra_df = pd.read_csv('C:\\Users\\franc\\Documents\\GitHub\\Listing_Investments_PT\\Main App\\Infrastructue_data\\Infrastructure.csv')

print(listings_df.columns)
print(infra_df.columns)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the earth specified by latitude and longitude.
    Returns distance in kilometers.
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Radius of the Earth in kilometers
    R = 6371.0
    distance = R * c

    return distance

# Create a matrix to store distances
distance_matrix = pd.DataFrame(index=listings_df.index, columns=infra_df.index)

for listing_idx, listing_row in listings_df.iterrows():
    for infra_idx, infra_row in infra_df.iterrows():
        distance = haversine_distance(listing_row['latitude'], listing_row['longitude'], 
                                      infra_row['latitude'], infra_row['longitude'])
        distance_matrix.at[listing_idx, infra_idx] = distance

# Store Pre-calculated Distances

# Save the distance matrix to the SQLite database
distance_matrix.to_sql('distance_matrix', conn, if_exists='replace')

# Close the database connection
conn.close()



