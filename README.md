# Real Estate Investment Opportunity Scraper

This project aims to scrape real estate listings from the Idealista website and stores them in a SQLite database. The goal is to identify potential investment opportunities in the real estate market.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Scraper](#scraper)
  - [SQLite Database](#sqlite-database)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.x
- BeautifulSoup4
- SQLite
- Requests

## Installation

Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/your-repo-name.git
```

Navigate to the project directory and install the required packages.

```bash
cd your-repo-name
pip install -r requirements.txt
```

## Usage

### Scraper

The scraper is implemented in Python and uses BeautifulSoup4 to parse HTML content. It fetches real estate listings from the Idealista website.

To run the scraper:

```bash
python scraper.py
```

This will start the scraper, and it will fetch listings from the Idealista website. The scraped data includes:

- Address
- Thumbnail
- Listing Price
- Listing Date
- Property Type
- State (New, Used, or To Be Built)
- Description
- URL
- Square Meters Built
- Total Square Meters
- Price Per Square Meter
- Number of Rooms
- Number of Baths
- Days in Market
- Garage
- Elevator

### SQLite Database

The scraped data is stored in a SQLite database for further analysis. The database schema is defined in `SQLite_db.py`.

To initialize the database:

```bash
python SQLite_db.py
```

This will create a new SQLite database with a `listings` table where the scraped data will be stored.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

[Insert your LICENSE here]
