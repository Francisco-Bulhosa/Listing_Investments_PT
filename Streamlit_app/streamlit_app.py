import streamlit as st
import pandas as pd


class DataLoader:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path, encoding="utf-8")
    
    def clean_data(self):
        # Implement cleaning logic here
        pass


class PropertyFilter:
    def __init__(self, data):
        self.data = data

    def filter_data(self, property_type, num_rooms, price_range):
        filtered_data = self.data[
            (self.data["property_type"] == property_type) &
            (self.data["number_of_rooms"] == num_rooms) &
            (self.data["listing_price"] >= price_range[0]) &
            (self.data["listing_price"] <= price_range[1])
        ]
        return filtered_data
    

class Visualizer:
    def __init__(self, data):
        self.data = data

    def show_visualizations(self):
        st.subheader("Visualization")
        st.bar_chart(self.data.groupby("property_type")["listing_price"].mean())


if __name__ == "__main__":
    # Load and clean data
    loader = DataLoader("C:/Users/franc/Documents/GitHub/Listing_Investments_PT/listings.csv")
    loader.clean_data()

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

    # Filter data
    property_filter = PropertyFilter(loader.data)
    filtered_data = property_filter.filter_data(selected_property_type, selected_number_of_rooms, selected_price_range)

    # Display filtered data
    st.write(f"Showing {len(filtered_data)} results")
    st.dataframe(filtered_data)

    # Visualizations
    visualizer = Visualizer(filtered_data)
    visualizer.show_visualizations()
