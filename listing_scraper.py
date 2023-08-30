import requests
from bs4 import BeautifulSoup
import time

def scrape_details(details_url):
    response = requests.get(details_url)
    if response.status_code == 200:
        details_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Pretty print a subset of the details page
        print(details_soup.prettify())
        
        # Scrape additional details here and return
        description = details_soup.find("div", class_="item-description description")
        if description is not None:
            return {"description": description.text}
        else:
            logging.info("Description not found in details page.")
            return None
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
                
                full_details_link = "https://www.idealista.pt/comprar-casas/almada/caparica-e-trafaria" + details_link
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