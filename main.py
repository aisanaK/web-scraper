import csv

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
        csv_writer.writerow(['title', 'price', 'stock'])
        books = soup.find_all(class_="product_pod")

        page_number = soup.find('li', class_='next').a
        print(page_number)

        for i in books:
            title = i.find("h3").a.get('title')
            price = i.find('div', class_='product_price').p.text
            in_stock = i.find(class_='instock availability').text.strip()
            book = {"title": title, "price": price, "stock": in_stock}
            print(book)
            csv_writer.writerow([title, price, in_stock])

        csv_file.close()


if __name__ == "__main__":
    main()
