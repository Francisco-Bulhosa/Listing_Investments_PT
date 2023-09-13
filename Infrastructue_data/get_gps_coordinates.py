from geopy.geocoders import Nominatim
import pandas as pd
import time

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="get_gps_coordinates.py")

# Function to get GPS coordinates given a place name
def get_coordinates(place_name):
    try:
        # Perform a search using the place name
        location = geolocator.geocode(place_name)
        
        # Check if location is None
        if location is None:
            print(f"No results found for {place_name}")
            return None
        
        # Extract the latitude and longitude
        lat = location.latitude
        lng = location.longitude
        
        return f"{lat}, {lng}"
    except Exception as e:
        print(f"An error occurred for {place_name}: {e}")
        return None

# Read the CSV file into a DataFrame
df = pd.read_csv('C:/Users/franc/Documents/GitHub/Listing_Investments_PT/Infrastructue_data/Infrastructure.csv', encoding="utf-8")


# Fetch the GPS coordinates for each infrastructure and store them in the DataFrame
df['gps_coordinates'] = df['infrastructure_names'].apply(get_coordinates)

# Introduce sleep to respect the API rate limits
time.sleep(1)

# Save the updated DataFrame to a new CSV file
df.to_csv('C:/Users/franc/Documents/GitHub/Listing_Investments_PT/Infrastructue_data/Infrastructure.csv', index=False)
