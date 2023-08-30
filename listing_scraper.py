import requests
from bs4 import BeautifulSoup
import time
import logging
import sqlite3 
from SQLite_db import initialize_database


def scrape_details(details_url):
    response = requests.get(details_url)
    if response.status_code == 200:
        details_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Pretty print a subset of the details page
        print(details_soup.prettify())
        
        # Initialize a dictionary to store scraped data
        scraped_data = {}

        # Scrape description
        description = details_soup.find("div", class_="item-description description")
        if description is not None:
            scraped_data["description"] = description.text

        # Scrape address
        address = details_soup.find("div", class_="item-address")
        if address is not None:
            scraped_data["address"] = address.text

        # Scrape listing price
        listing_date = details_soup.find("div", class_="item-price")
        if price is not None:
            scraped_data["listing_price"] = price.text

            # Scrape listing date
        listing_date = details_soup.find("div", class_="listing-date")
        if listing_date:
            scraped_data["listing_date"] = listing_date.text.strip()

        # Scrape property type
        property_type = details_soup.find("div", class_="property-type")
        if property_type:
            scraped_data["property_type"] = property_type.text.strip()

        # Scrape state (New, Used, etc.)
        state = details_soup.find("div", class_="property-state")
        if state:
            scraped_data["state"] = state.text.strip()

        # Scrape URL 
        scraped_data["url"] = details_url

        # Scrape square meters built
        square_meters_built = details_soup.find("div", class_="square-meters-built")
        if square_meters_built:
            scraped_data["square_meters_built"] = float(square_meters_built.text.strip().replace(" m²", ""))

        # Scrape total square meter
        total_sq_meter = details_soup.find("div", class_="total-square-meter")
        if total_sq_meter:
            scraped_data["total_sq_meter"] = float(total_sq_meter.text.strip().replace(" m²", ""))

        # Scrape price per square meter
        price_per_sq_meter = details_soup.find("div", class_="price-per-sq-meter")
        if price_per_sq_meter:
            scraped_data["price_per_sq_meter"] = float(price_per_sq_meter.text.strip().replace(" €/m²", ""))

        # Scrape number of rooms
        number_of_rooms = details_soup.find("div", class_="number-of-rooms")
        if number_of_rooms:
            scraped_data["number_of_rooms"] = int(number_of_rooms.text.strip().replace(" rooms", ""))

        # Scrape number of baths
        number_of_baths = details_soup.find("div", class_="number-of-baths")
        if number_of_baths:
            scraped_data["number_of_baths"] = int(number_of_baths.text.strip().replace(" baths", ""))

        # Scrape days in market
        days_in_market = details_soup.find("div", class_="days-in-market")
        if days_in_market:
            scraped_data["days_in_market"] = int(days_in_market.text.strip().replace(" days", ""))


        return scraped_data
    else:
        logging.info(f"Failed to retrieve details page with status code {response.status_code}")
        return None
        

# Starting URL
start_url = "https://www.idealista.pt/comprar-casas/almada/caparica-e-trafaria/"

 while start_url:
    # Make a request to the Idealista website
    response = requests.get(start_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Pretty print the entire page (you might want to comment this out after verifying)
        print(soup.prettify())
        
        # Find listings based on the article tag and classes
        listings = soup.find_all("a", class_="item-link")
        
        # Debugging with intermediate variables
        num_listings = len(listings)
        logging.info(f"Found {num_listings} listings on this page.")
        
        for listing in listings:
            # Pretty print each listing
            print(listing.prettify())
            
            # Extract link to details page
            details_link_element = listing.find("a", role="heading")
            
            # Check for None
            if details_link_element is not None:
                details_link = details_link_element["href"]
                
                # Debugging with intermediate variable
                logging.info(f"Fetching details from {details_link}")
                
                full_details_link = "https://www.idealista.pt/" + details_link
                details_data = scrape_details(full_details_link)
                
                # Print the scraped details
                print(details_data)
            else:
                logging.info("Details link not found in listing.")







        # Find the next page link
        next_page_element = soup.find("a", {"rel": "nofollow", "class": "icon-arrow-right-after"})
        
        # Check for None
        if next_page_element is not None:
            next_page = next_page_element["href"]
            start_url = "https://www.idealista.pt/comprar-casas/almada/caparica-e-trafaria/" + next_page
        else:
            logging.info("Next page not found. Exiting.")
            start_url = None

        # Sleep for a short time to respect the website's rate-limiting
        time.sleep(5)
    else:
        print("Failed to retrieve the webpage")
        start_url = None

