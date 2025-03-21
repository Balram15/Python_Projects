import requests
from bs4 import BeautifulSoup
import csv


def scrape_quotes():
    url = 'http://quotes.toscrape.com/page/{}/'
    quotes_data = []
    page = 1

    while True:
        response = requests.get(url.format(page))
        if response.status_code != 200:
            print("No more pages or failed to fetch data.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')

        if not quotes:
            break

        for i in range(len(quotes)):
            quote_text = quotes[i].text
            author_text = authors[i].text
            quotes_data.append([quote_text, author_text])
            print(f"Quote: {quote_text}")
            print(f"Author: {author_text}")
            print("-" * 50)

        page += 1

    save_to_csv(quotes_data)


def save_to_csv(data):
    try:
        with open('quotes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Quote", "Author"])
            writer.writerows(data)
        print("Data saved to quotes.csv")
    except Exception as e:
        print(f"Error while saving data: {e}")


if __name__ == '__main__':
    scrape_quotes()
