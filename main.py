import csv

import requests
from bs4 import BeautifulSoup

list = ['Title', 'Price', 'Stock', 'Link', 'UPC', 'Product Type', 'Price', 'Price with Tax', 'Tax', 'Availability', 'Number of Reviews']
max_price = 0
min_price = 1000000
def main():
    csv_file = open("books_toscrape.csv", "a")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(list)
    
    for page_number in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"


        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')  # BeautifulSoup constructor

        books = soup.find_all(class_="product_pod")

        for book in books:
            # title
            title = book.find("h3").a.get('title')
            print(title)

            # price
            price = book.find('div', class_='product_price').p.text
            price_float = float(price[2:])
            print(price_float)

            if price_float > max_price:
                max_price = price_float
            if price_float < min_price:
                min_price = price_float



            # link to open each book
            link = 'https://books.toscrape.com/catalogue/' + book.find('a').get('href')
            in_stock = book.find(class_='instock availability').text.strip()

            # open_book constructor
            open_link = requests.get(link).text
            soup = BeautifulSoup(open_link, 'lxml')
            open_book = soup.find(class_="product_page")

            
            table = []
            for list1 in range(1, 8):
                table.append(
                    open_book.select_one(f'table tr:nth-child({list1}) td').text.strip()
                )
            csv_writer.writerow([title, price_float, in_stock, link, *table])
        print('Maximum price is', max_price)
        print('Minimum price is', min_price)
    csv_file.close()
    

print(max_price)

if __name__ == "__main__":
    main()
