from Infrastructue_data.get_listings import create_connection

class Listing:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def display(self):
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")


def fetch_listings_from_db():
    conn = create_connection()
    if not conn:
        return []

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM listings")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    listings = [Listing(**dict(zip(columns, row))) for row in rows]
    
    conn.close()

    return listings

# Test the functionality
if __name__ == "__main__":
    listings = fetch_listings_from_db()
    for listing in listings[:5]:  # Displaying the first 5 listings as an example
        listing.display()
        print('-' * 30)