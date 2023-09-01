import sqlite3

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
        url TEXT,
        square_meters_built REAL,
        total_sq_meter REAL,
        price_per_sq_meter REAL,
        number_of_rooms INTEGER,
        number_of_baths INTEGER,
        with_elevator INTEGER DEFAULT 0, 
        with_garage INTEGER DEFAULT 0,
        living_rooms INTEGER,
        kitchens INTEGER,
        description TEXT
    );
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()

