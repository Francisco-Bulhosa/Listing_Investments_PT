
import sqlite3
import sys
from paths import LISTINGS_DB_PATH

def create_connection():
    """
    Create a database connection to the SQLite database.
    
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(LISTINGS_DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}: Could not establish a connection to the database.")
        return None

