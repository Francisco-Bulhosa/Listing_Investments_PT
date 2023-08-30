import requests
from bs4 import BeautifulSoup

# Make a request to the Idealista website (Replace with the actual URL)
response = requests.get("https://www.idealista.pt/comprar-casas/almada/caparica-e-trafaria/")
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find listings (Replace with the actual HTML tag and class or ID that wraps each listing)
    listings = soup.find_all("div", class_="listing-wrapper")
    
    for listing in listings:
        # Extract data fields (Replace with the actual HTML tags and classes or IDs that contain each data field)
        address = listing.find("span", class_="address-class").text if listing.find("span", class_="address-class") else None
        thumbnail = listing.find("img", class_="thumbnail-class")["src"] if listing.find("img", class_="thumbnail-class") else None
        price = listing.find("span", class_="price-class").text if listing.find("span", class_="price-class") else None
        # ... and so on for other fields
        
        # Store or print the data
        print(f"Address: {address}, Thumbnail: {thumbnail}, Price: {price}")
