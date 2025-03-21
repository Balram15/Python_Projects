Web Scraper Project

This project is a simple web scraper built using Python, requests, and BeautifulSoup to extract quotes and their authors from the website Quotes to Scrape. It supports pagination, error handling, and saves the extracted data to a CSV file.

Features

Scrapes quotes and authors from multiple pages.

Saves data to quotes.csv.

Handles errors gracefully.

Provides clear console output.

Requirements

Ensure you have Python installed and the necessary libraries:

pip install requests beautifulsoup4

How to Run

Clone this repository:

git clone https://github.com/Balram15/web-scraper.git

Navigate to the project directory:

cd web-scraper

Run the scraper:

python web_scraper.py

Check the output in quotes.csv.


Error Handling

If the website is unreachable or if there are no quotes on a page, an error message will be displayed.

The scraper will stop when no more pages are available.

Project Structure

web-scraper/
│
├── web_scraper.py
├── quotes.csv
└── README.md

Contributing

Feel free to fork this project and submit pull requests.

