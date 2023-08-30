import requests
from bs4 import BeautifulSoup
import time

def scrape_details(details_url):
    response = requests.get(details_url)
    if response.status_code == 200:
        details_soup = BeautifulSoup(response.text, 'html.parser')
        # Scrape additional details here and return
        # For example:
        description = details_soup.find("div", class_="item-description description").text if details_soup.find("div", class_="item-description description") else None
        return {"description": description}
    else:
        return None

# Starting URL
start_url = "https://www.idealista.pt/comprar-casas/almada/caparica-e-trafaria/"

while start_url:
    # Make a request to the Idealista website
    response = requests.get(start_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find listings based on the article tag and classes
        listings = soup.find_all("article", class_="item")
        
        for listing in listings:
            # Extract link to details page
            details_link = listing.find("a", role="heading")["href"] if listing.find("a", role="heading") else None
            if details_link:
                full_details_link = "https://www.idealista.com" + details_link
                details_data = scrape_details(full_details_link)
                
                # Print the scraped details
                print(details_data)

        # Find the next page link
        next_page = soup.find("a", {"rel": "nofollow", "class": "icon-arrow-right-after"})["href"] if soup.find("a", {"rel": "nofollow", "class": "icon-arrow-right-after"}) else None
        start_url = "https://www.idealista.com" + next_page if next_page else None
        
        # Sleep for a short time to respect the website's rate-limiting
        time.sleep(2)
    else:
        print("Failed to retrieve the webpage")
        start_url = None