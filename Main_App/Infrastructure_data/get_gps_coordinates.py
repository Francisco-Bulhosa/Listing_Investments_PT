from geopy.geocoders import Nominatim
import pandas as pd
import time

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="get_gps_coordinates.py")

# Function to get GPS coordinates given a place name
def get_coordinates(place_name):
    try:
        location = geolocator.geocode(place_name)
        if location is None:
            print(f"No results found for {place_name}")
            return None, None
        return location.latitude, location.longitude
    except Exception as e:
        print(f"An error occurred for {place_name}: {e}")
        return None, None

# Read the CSV file into a DataFrame
df = pd.read_csv('C:/Users/franc/Documents/GitHub/Listing_Investments_PT/Infrastructue_data/Infrastructure.csv', encoding="utf-8")


# Fetch the GPS coordinates for each infrastructure and store them in the DataFrame
df['latitude'], df['longitude'] = zip(*df['infrastructure_names'].apply(get_coordinates))

# Introduce sleep to respect the API rate limits
time.sleep(1)

# Save the updated DataFrame to a new CSV file
df.to_csv('C:/Users/franc/Documents/GitHub/Listing_Investments_PT/Infrastructue_data/Infrastructure.csv', index=False)
