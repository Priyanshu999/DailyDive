import requests
from bs4 import BeautifulSoup

r = requests.get("https://timesofindia.indiatimes.com/india")

soup = BeautifulSoup(r.text, 'lxml')

# print(soup.prettify())

for article in soup.find_all('div', class_='iN5CR'):
    article_link = article.a['href']
    r2 = requests.get(article_link).text
    soup2 = BeautifulSoup(r2, 'lxml')
    print(soup2.h1.text)