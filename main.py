import csv
import requests
from bs4 import BeautifulSoup

list = ['Title', 'Price', 'Stock', 'Link', 'UPC', 'Product Type', 'Price', 'Price with Tax', 'Tax', 'Availability', 'Number of Reviews']
max_price = 0
min_price = 0
def main():
    for page_number in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"


        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')  # BeautifulSoup constructor

        # csv file
        csv_file = open("books_toscrape.csv", "a")
        csv_writer = csv.writer(csv_file)

        if page_number == 1:
            csv_writer.writerow(list)

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
                price_float = max_price
            if price_float < min_price:
                price_float = min_price



            # link to open each book
            link = 'https://books.toscrape.com/catalogue/' + book.find('a').get('href')
            in_stock = book.find(class_='instock availability').text.strip()

            # open_book constructor
            open_link = requests.get(link).text
            soup = BeautifulSoup(open_link, 'lxml')
            open_book = soup.find(class_="product_page")

            # table in book
            for list1 in range(1, 8):
                table = open_book.select_one(f'table tr:nth-child({list1})').text.strip()
                print(table)

            # ipdb.set_trace()

            # table = open_book.find(class_='table table-striped').text

            # book = {"Title": title, "Stock": in_stock, 'Link': url}
            # print(book)

        csv_writer.writerow(list)

        csv_file.close()

print(max_price)

if __name__ == "__main__":
    main()
