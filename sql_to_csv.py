import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect("listings.db")
cursor = conn.cursor()

# Execute a SELECT query to retrieve data from the table
query = "SELECT * FROM listings"
cursor.execute(query)

# Get the column names from the cursor's description
columns = [column[0] for column in cursor.description]

# Fetch and write the data in chunks to the CSV file
csv_filename = "listings.csv"
with open(csv_filename, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header (column names)
    csv_writer.writerow(columns)
    
    # Fetch and write data in chunks
    chunk_size = 1000  # Adjust this to your preference
    while True:
        rows = cursor.fetchmany(chunk_size)
        if not rows:
            break
        csv_writer.writerows(rows)

print(f"CSV file '{csv_filename}' created successfully.")

# Close the database connection
conn.close()