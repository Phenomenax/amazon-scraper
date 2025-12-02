# Amazon Product Scraper

A simple and efficient Python Web Scraper to scrape product data from Amazon Australia. This tool searches for a specified product, extracts key details, and lists the top 5 cheapest options available.

## Features

- **Search Functionality**: Queries Amazon AU for any product name provided by the user.
- **Data Extraction**: Retrieves product titles, prices, and direct links.
- **Smart Sorting**: Automatically sorts results to display the 5 most affordable options.
- **Anti-Bot Measures**: Uses `fake-useragent` to rotate user agents and mimic real browser behavior.
- **Debugging Support**: Saves HTML snapshots (`debug.html` or `debug_blocked.html`) to help troubleshoot layout changes or blocking issues.

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script from your terminal:

   ```bash
   python scraper.py
   ```

2. Enter the product name when prompted (e.g., "wireless headphones").
3. View the top 5 cheapest results printed in the terminal.

## Disclaimer

This tool is for **personal purposes only**. Web scraping may violate Amazon's Terms of Service. The author is not responsible for any misuse of this software or any potential consequences resulting from its use. Use responsibly and respect the website's `robots.txt` and policies.
