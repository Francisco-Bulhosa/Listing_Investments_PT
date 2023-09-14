from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import streamlit as st

class Geocoder:
    def __init__(self, user_agent="geoapiExercises"):
        self.geolocator = Nominatim(user_agent=user_agent)

    def get_lat_lon(self, address):
        location = self.geolocator.geocode(address)
        return location.latitude, location.longitude


class MapPlotter:
    def __init__(self, geocoder):
        self.geocoder = geocoder

    def plot_map(self, address):
        latitude, longitude = self.geocoder.get_lat_lon(address)
        m = folium.Map(location=[latitude, longitude], zoom_start=15)
        folium.Marker([latitude, longitude], popup=address).add_to(m)
        folium_static(m)


class RealEstateApp:
    def __init__(self):
        self.geocoder = Geocoder()
        self.map_plotter = MapPlotter(self.geocoder)

    def run(self):
        st.title("Real Estate Investment Analysis")
        
        # Get address from user
        address = st.text_input("Enter an address:", "1600 Amphitheatre Parkway, Mountain View, CA")
        
        # Plot map
        self.map_plotter.plot_map(address)