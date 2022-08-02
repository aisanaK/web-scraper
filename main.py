from bs4 import BeautifulSoup
import requests
import csv

url = "https://books.toscrape.com/catalogue/page-1.html"
print(url)

source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')  # BeautifulSoup constructor

# csv file
csv_file = open("books_toscrape.csv", "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['title', 'price', 'stock'])
books = soup.find_all(class_="product_pod")


page = soup.find('li', class_='next').a
print(page)

for i in books:
    title = i.find("h3").a.get('title')
    price = i.find('div', class_='product_price').p.text
    in_stock = i.find(class_='instock availability').text.strip()
    book = {"title": title, "price": price, "stock": in_stock}
    print(book)
    csv_writer.writerow([title, price, in_stock])



csv_file.close()


