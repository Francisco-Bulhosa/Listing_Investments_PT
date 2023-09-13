import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

class DataLoader:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path, encoding="utf-8")
    
    def clean_data(self):
        # Implement cleaning logic here
        pass


class PropertyFilter:
    def __init__(self, data):
        self.data = data

    def filter_data(self, property_type, num_rooms, price_range, user_budget=None, build_or_rent="Any", important_infrastructure="Any"):
        # Initialize with existing filters
        filtered_data = self.data[
            (self.data["property_type"] == property_type) &
            (self.data["number_of_rooms"] == num_rooms) &
            (self.data["listing_price"] >= price_range[0]) &
            (self.data["listing_price"] <= price_range[1])
        ]
        
        # Budget filter, if specified
        if user_budget is not None:
            filtered_data = filtered_data[filtered_data['listing_price'] <= user_budget]
        
        # Build or Rent filter, if specified
        if build_or_rent != "Any":
            filtered_data = filtered_data[filtered_data['property_intent'] == build_or_rent]
        
        # Infrastructure filter, if specified
        if important_infrastructure != "Any":
            sorted_data = filtered_data.sort_values(by=f'distance_to_{important_infrastructure.lower()}', ascending=True)
            filtered_data = sorted_data  # Update filtered_data with sorted data
        
        # Select Top 10
        top_10_data = filtered_data.head(10)
        
        return top_10_data
    

class Visualizer:
    def __init__(self, data):
        self.data = data

    def show_visualizations(self):
        st.subheader("Visualization")
        st.bar_chart(self.data.groupby("property_type")["listing_price"].mean())


class Geocoder:
    def __init__(self, user_agent="geoapiExercises"):
        self.geolocator = Nominatim(user_agent=user_agent)

    def get_lat_lon(self, address):
        location = self.geolocator.geocode(address)
        return location.latitude, location.longitude



class MapPlotter:
    def __init__(self, geocoder):
        self.geocoder = geocoder

    def plot_map(self, df):
        # Initialize a base map
        m = folium.Map(location=[38.6431, -9.2096], zoom_start=12)  # Initialized to Almada; you can change this

        # Loop through each address in the DataFrame
        for _, row in df.iterrows():
            address = row['address']
            try:
                latitude, longitude = self.geocoder.get_lat_lon(address)
                folium.Marker([latitude, longitude], popup=address).add_to(m)
            except:
                print(f"Could not geocode address: {address}")

        # Display the map in Streamlit
        folium_static(m)



if __name__ == "__main__":
    # Load and clean data
    loader = DataLoader("C:/Users/franc/Documents/GitHub/Listing_Investments_PT/listings.csv")
    loader.clean_data()
    geocoder = Geocoder()
    map_plotter = MapPlotter(geocoder)

    # Streamlit UI
    st.title("Real Estate Investment Analysis")
    st.sidebar.title("Filters")

    selected_property_type = st.sidebar.selectbox("Select Property Type", loader.data["property_type"].unique())
    selected_number_of_rooms = st.sidebar.selectbox("Select number of Bedrooms", loader.data["number_of_rooms"].unique())
    selected_price_range = st.sidebar.slider("Select Price Range",
                                                int(min(loader.data["listing_price"])),
                                                int(max(loader.data["listing_price"])),
                                                (int(min(loader.data["listing_price"])), int(max(loader.data["listing_price"])))
                                            )



    # New User Input Widgets
    user_budget = st.sidebar.number_input("How much do you intend to spend?", min_value=10000, max_value=100000000, step=1000)
    build_or_rent = st.sidebar.selectbox("Do you wish to build or just rent?", ["Build", "Rent"])
    important_infrastructure = st.sidebar.selectbox("Which infrastructure is most important for you?", 
                                                    ["Zones", "Universities", "Metro Station", "Hospitals", "Train Station", "Beach"])


    # Filter data
    property_filter = PropertyFilter(loader.data)
    filtered_data = property_filter.filter_data(selected_property_type, selected_number_of_rooms, selected_price_range, user_budget, build_or_rent, important_infrastructure)


    # Display filtered data
    st.write(f"Showing {len(filtered_data)} results")
    st.dataframe(filtered_data)

    # Plot map based on the filtered data
    map_plotter.plot_map(filtered_data)

    # Visualizations
    visualizer = Visualizer(filtered_data)
    visualizer.show_visualizations()
