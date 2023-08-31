import requests
from bs4 import BeautifulSoup
import time
import logging
import sqlite3 
from SQLite_db import initialize_database



def initialize_database():
    conn = sqlite3.connect("listings.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        thumbnail TEXT,
        listing_price TEXT,
        listing_date TEXT,
        property_type TEXT,
        construction_year TEXT,
        state TEXT,
        description TEXT,
        url TEXT,
        square_meters_built REAL,
        total_sq_meter REAL,
        price_per_sq_meter REAL,
        number_of_rooms INTEGER,
        number_of_baths INTEGER,
        days_in_market INTEGER,
        with_elevator INTEGER DEFAULT 0, 
        with_garage INTEGER DEFAULT 0 
    );
    """)
    
    conn.commit()
    conn.close()



def insert_into_database(data):
    conn = sqlite3.connect("listings.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO listings (
        address, thumbnail, listing_price, listing_date, property_type, construction_year, state,
        description, url, square_meters_built, total_sq_meter, price_per_sq_meter,
        number_of_rooms, number_of_baths, days_in_market, with_elevator, with_garage
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('address'), data.get('thumbnail'), data.get('listing_price'), 
        data.get('listing_date'), data.get('property_type'), data.get('total_sq_meter'), data.get('state'), 
        data.get('description'), data.get('url'), data.get('square_meters_built'),
        data.get('total_sq_meter'), data.get('price_per_sq_meter'), data.get('number_of_rooms'),
        data.get('number_of_baths'), data.get('days_in_market'), data.get('with_elevator', 0),
        data.get('with_garage', 0)
    ))
    conn.commit()
    conn.close()


def scrape_details(details_url):
    response = requests.get(details_url)
    if response.status_code == 200:
        details_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize a dictionary to store scraped data
        scraped_data = {}

        # Scrape description
        description = details_soup.find("h1", class_="property-title")
        if description is not None:
            scraped_data["description"] = description.text


        # Locate the h2 element with the text "Localização"
        localizacao_header = details_soup.find("div", string="detail-info-map-info")

        # Check if the header was found
        if localizacao_header:
            # Find the next <ul> sibling element
            span_element = localizacao_header.find_next_sibling("div")
            
            # Find all the <li> elements with class "header-map-list" under this <ul>
            address_elements = span_element.find_all("div", class_="header-map-list") if ul_element else []
            
            # Check if any address elements were found
            if address_elements:
                address_parts = [elem.text.strip() for elem in address_elements]
                complete_address = ', '.join(address_parts)
                scraped_data["address"] = complete_address

        # Scrape listing price
        listing_price = details_soup.find("div", class_="property-price")
        if listing_price is not None:
            scraped_data["listing_price"] = listing_price.text.strip()

            # Scrape listing date
        listing_date = details_soup.find("p", class_="stats-text")
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

        # Find all the <span> elements under <div class="info-features">
        info_features = details_soup.find("div", class_="detail-property-info")
        if info_features:
            feature_spans = info_features.find_all("span")
            for feature in feature_spans:
                feature_text = feature.text.strip().lower()  # Convert to lowercase for easier comparison
                if "m²" in feature_text:
                    scraped_data["square_meters_built"] = feature_text.replace(" m² área bruta", "")
                elif "quartos" in feature_text:
                    scraped_data["number_of_rooms"] = feature_text.replace("", "quartos") # number of habitable divisions
                elif "Com elevador" in feature_text:
                    scraped_data["with_elevator"] = True # If it has or not an elevator
                elif "Com garagem" in feature_text:
                    scraped_data["with_garage"] = True # if it has a garage
                elif "Ano construção:" in feature_text:
                    scraped_data[""]

        # # Scrape total square meter
        # total_sq_meter = details_soup.find("div", class_="total-square-meter")
        # if total_sq_meter:
        #     scraped_data["total_sq_meter"] = float(total_sq_meter.text.strip().replace(" m²", ""))

        price_per_sq_meter_div = details_soup.find('div', class_='detail-info-counter-txt')

        if price_per_sq_meter_div:
            # Find the 'strong' element inside the 'div'
            strong_element = price_per_sq_meter_div.find('strong')
            
            # Check if the strong element is found and contains '€ / m²'
            if strong_element and '€ / m²' in strong_element.text:
                price_per_sq_meter_text = strong_element.text.strip()
                
                # Clean up the text to extract the numeric value, remove the ' €/m²' part and convert to float
                price_per_sq_meter = float(price_per_sq_meter_text.replace(' € / m²', '').replace('.', '').replace(',', '.'))
                
                # Now `price_per_sq_meter` contains the numeric value
            else:
                price_per_sq_meter = None
        else:
            # Handle the case where the element was not found
            price_per_sq_meter = None

        # Scrape days in market
        days_in_market = details_soup.find("p", class_="date-update-text")
        if days_in_market:
            days_text = days_in_market.text.strip()  # Gets "Anuncio atualizado há x dias"
            days_number = int(days_text.split()[-2])  # Splits the text and picks the second last word, which should be "x" and converts it to int
            scraped_data["days_in_market"] = days_number  # Stores it in the dictionary
              
              
    
        # Logging to show the scraped data
        logging.info("Scraped Data:")
        for key, value in scraped_data.items():
            logging.info(f"{key}: {value}")


        return scraped_data
    else:
        logging.info(f"Failed to retrieve details page with status code {response.status_code}")
        return None
    

        

if __name__ == "__main__":
    initialize_database()
    logging.basicConfig(level=logging.INFO)


    # Starting URL
    start_url = "https://supercasa.pt/comprar-casas/almada/caparica-e-trafaria"


    # Counter for the number of listings scraped
    count = 0
    max_count = 5  # Maximum number of listings to scrape


    while start_url and count < max_count:  # Modified this line to include count < max_count
    # while start_url:
        # Make a request to the Idealista website
        response = requests.get(start_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find listings based on the article tag and classes
            listings = soup.find_all("div", class_="property-info")
            
            # Debugging with intermediate variables
            num_listings = len(listings)
            logging.info(f"Found {num_listings} listings on this page.")


            # LUuuuIIIISS!!! ISto pode ficar preso aqui se ele não encontrar listings??????????????????????????????????????????
            
            for listing in listings:

                # Extract link to details page
                details_link_element = listing.find("h2", class_="property-list-title")
                if details_link_element:
                    details_link = details_link_element.find("a")

                    if details_link:
                        details_link = details_link.get("href")
                        # Check for None
                        if details_link is not None:
                            # Debugging with intermediate variable
                            logging.info(f"Fetching details from {details_link}")
                            
                            full_details_link = "https://supercasa.pt" + details_link
                            details_data = scrape_details(full_details_link)
                            
                            if details_data:  # Check if details were successfully scraped
                                insert_into_database(details_data)  # Insert data into the database
                                

                                # Increase the count for each listing processed
                                count += 1
                                
                                if count > max_count:  # New condition
                                    break  # Break the loop if maximum count reached

                                    # Print the scraped details
                                    print(details_data)
                            else:
                                logging.info("Failed to scrape details for this listing.")

                else:
                    logging.warning(f"No <a> tag found in details link element: {details_link_element}")

            else:
                logging.warning(f"No details link element found in listing:\n{listing}")
 



        if count >= max_count:  # New condition
            logging.info(f"Reached the maximum count of {max_count}. Exiting.")
            break  # Break the loop if maximum count reached


        
        # Find the next page link
        next_page_element = soup.find("a", {"class": "list-pagination-next", "title" : "Seguinte"})
        
        # Check for None
        if next_page_element is not None:
            next_page = next_page_element["href"]
            start_url = "https://supercasa.pt" + next_page
        else:
            logging.info("Next page not found. Exiting.")
            start_url = None

        # Sleep for a short time to respect the website's rate-limiting
        time.sleep(8)
    else:
        logging.info("Failed to retrieve the webpage")
        start_url = None

 