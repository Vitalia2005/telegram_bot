from bs4 import BeautifulSoup
import requests
import csv

def save():
    pages = 'https://citaty.info/book?page='
    # обработаем с сайта первые 3 страницы с цитатами и скачаем цитаты из них в csv файл

    for i in range(3):
        request = requests.get(pages+str(i))
        b = BeautifulSoup(request.text, "html.parser")
        p3 = b.find_all("div", {"class": "field-item even last"})
        author = b.find_all('a', {'title': 'Автор цитаты'})
        book = b.find_all('a', {'title': 'Цитата из книги'})
        with open('quotes_book.csv',   mode="w", encoding='utf-8') as file:

            file_writer = csv.writer(file)
            file_writer.writerow(['Цитата', 'Автор', 'Книга'])
            for k in range(len(p3)):
                print(p3[k].get_text())
                file_writer.writerow([p3[k].get_text().strip(), author[k].get_text(), book[k].get_text()])
    return p3


save()