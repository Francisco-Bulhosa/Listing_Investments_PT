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
        timestamp TEXT DEFAULT (strftime('%Y-%m-%d %H:00', 'now')),
        address TEXT,
        thumbnail TEXT,
        listing_price TEXT,
        listing_date TEXT,
        property_type TEXT,
        construction_year INTEGER,
        state TEXT,
        url TEXT,
        square_meters_built REAL,
        total_sq_meter REAL,
        price_per_sq_meter REAL,
        number_of_rooms INTEGER,
        number_of_baths INTEGER,
        with_elevator INTEGER DEFAULT 0, 
        with_garage INTEGER DEFAULT 0,
        description TEXT
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
         url, square_meters_built, total_sq_meter, price_per_sq_meter,
        number_of_rooms, number_of_baths, with_elevator, with_garage, description
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('address'), data.get('thumbnail'), data.get('listing_price'), 
        data.get('listing_date'), data.get('property_type'), data.get('construction_year'), data.get('state'), 
        data.get('url'), data.get('square_meters_built'),
        data.get('total_sq_meter'), data.get('price_per_sq_meter'), data.get('number_of_rooms'),
        data.get('number_of_baths'), data.get('with_elevator', 0),
        data.get('with_garage', 0), data.get('description')
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
        description_element = details_soup.find("div", class_="detail-info-description-txt")
        if description_element:
            description_text = description_element.get_text(strip=True)
            scraped_data["description"] = description_text


        # Locate the div element with class "detail-info-map-info"
        address_div = details_soup.find("div", class_="detail-info-map-info")

        # Check if the address div was found
        if address_div:
            # Extract the text from the address div
            address_text = address_div.get_text(strip=True)
            
            # Split the text by line breaks to get individual address parts
            address_parts = address_text.split("<br>")
            
            # Remove any leading or trailing whitespace from each address part
            address_parts = [part.strip() for part in address_parts]
            
            # Join the address parts with commas to create the complete address
            complete_address = ", ".join(address_parts)
            
            # Store the complete address in the scraped_data dictionary
            scraped_data["address"] = complete_address

        else:
            # Log an error message if address extraction fails
            logging.error("Failed to extract address from the page.")

        # Scrape listing price
        listing_price_element = details_soup.find("div", class_="property-price")
        if listing_price_element is not None:
            # Get the text of the span element
            listing_price_text = listing_price_element.get_text(strip=True)
            
            # Remove unwanted characters (e.g., "€" and extra text)
            listing_price_cleaned = listing_price_text.replace("€", "").replace("Simular prestação", "").strip()

            # Convert the cleaned listing price to a float and round to two decimal places
            listing_price = round(float(listing_price_cleaned), 2)
            
            # Store the cleaned listing price in the scraped_data dictionary
            scraped_data["listing_price"] = listing_price


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

        # Find all the <span> elements under <div class="property-features">
        info_features = details_soup.find("div", class_="property-features")
        if info_features:
            feature_spans = info_features.find_all("span")
            for feature in feature_spans:
                feature_text = feature.text.strip()
                
                # For square_meters_built
                if "Área bruta" in feature_text and "m²" in feature_text:
                    try:
                        square_meters_built = float(feature_text.replace("Área bruta", "").replace("m²", "").strip())
                        scraped_data["square_meters_built"] = square_meters_built
                    except ValueError:
                        logging.error("Failed to convert square_meters_built to float.")
                
                # For number_of_rooms
                elif "quartos" in feature_text:
                    try:
                        number_of_rooms = int(feature_text.replace(" quartos", "").strip())
                        scraped_data["number_of_rooms"] = number_of_rooms
                    except ValueError:
                        logging.error("Failed to convert number_of_rooms to int.")
                
                # For construction_year
                elif "Ano construção:" in feature_text:
                    try:
                        construction_year = int(feature_text.replace("Ano construção:", "").strip())
                        scraped_data["construction_year"] = construction_year
                    except ValueError:
                        logging.error("Failed to convert construction_year to int.")



        # Scrape Extended details 
        # Initialize to None before the loop
        scraped_data["with_elevator"] = None
        scraped_data["with_garage"] = None

        # Find all the <span> elements under <div class="info-features">
        info_features_extended = details_soup.find("div", class_="property-features highlights")
        if info_features_extended:
            feature_spans_extended = info_features_extended.find_all("span")
            for feature_extended in feature_spans_extended:
                feature_text_extended = feature_extended.text.strip()
                if "Com elevador" in feature_text_extended:
                    scraped_data["with_elevator"] = True  # If it has or not an elevator
                elif "Com garagem" in feature_text_extended:
                    scraped_data["with_garage"] = True  # if it has a garage
                else:
                    scraped_data["with_elevator"] = None
                    scraped_data["with_garage"] = None
                    logging.error("Failed to extract extended details from the page.")    
        # Check if data for "Com elevador" and "Com garagem" was not scraped
        if scraped_data["with_elevator"] is None or scraped_data["with_garage"] is None:
            logging.error("Failed to extract extended details for 'Com elevador' or 'Com garagem'.")
        



        # Scrape total square meter
        total_sq_meter = None  # Initialize the variable
        area_bruta_element = details_soup.find("li", class_="key-feature", string="Área Bruta")
        if area_bruta_element:
            area_bruta_text = area_bruta_element.text.strip()
            try:
                total_sq_meter = float(area_bruta_text.replace("Área Bruta :", "").replace("m2", "").strip())
                scraped_data["total_sq_meter"] = total_sq_meter
            except ValueError:
                # Log an error message if conversion to float fails
                logging.error("Failed to convert total sq/meter to float.")
        else:
            scraped_data["total_sq_meter"] = None
            # Log an error message if total sq meter extraction fails
            logging.error("Failed to extract total sq/meter from the page.")


        # Calculate price per square meter
        if listing_price is not None and total_sq_meter is not None:
            price_per_sq_meter = listing_price / total_sq_meter
            scraped_data["price_per_sq_meter"] = price_per_sq_meter
        else:
            price_per_sq_meter = None
            # Log an error message if total sq meter extraction fails
            logging.error("Failed to extract price_per_sq_meter from the page.")


    

        # Scrape days in market
        days_in_market = details_soup.find("p", class_="property-lastupdate")
        if days_in_market:
            days_text = days_in_market.text.strip()  # Gets "Anúncio atualizado no dia 30 de agosto"
            
            # Extract the date from the text
            date_str = days_text.split(" no dia ")[-1]
            
            # Parse the date using a datetime format that matches the text format
            from datetime import datetime
            date = datetime.strptime(date_str, "%d de %B")
            
            # Calculate the days difference between the scraped date and today's date
            days_difference = (datetime.now() - date).days
            
            scraped_data["days_in_market"] = days_difference  # Stores it in the dictionary
              
              
    
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
    max_count = 10  # Maximum number of listings to scrape


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