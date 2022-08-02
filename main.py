import csv

import ipdb
import requests
from bs4 import BeautifulSoup


def main():
    for page_number in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
        print(url)

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')  # BeautifulSoup constructor

        # csv file
        csv_file = open("books_toscrape.csv", "a")
        csv_writer = csv.writer(csv_file)

        if page_number == 1:
            csv_writer.writerow(['title', 'price', 'stock', 'link'])

        books = soup.find_all(class_="product_pod")

        for book in books:
            title = book.find("h3").a.get('title')
            price = book.find('div', class_='product_price').p.text
            link = 'https://books.toscrape.com/catalogue/' + book.find('a').get('href')

            # TODO: scrape each book
            # example
            # source = requests.get(link).text

            in_stock = book.find(class_='instock availability').text.strip()
            book = {"title": title, "price": price, "stock": in_stock, 'link': link}
            print(book)
            csv_writer.writerow([title, price, in_stock, link])

        csv_file.close()


if __name__ == "__main__":
    main()
