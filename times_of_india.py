import textwrap
import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get("https://timesofindia.indiatimes.com/india")
soup = BeautifulSoup(r.text, 'lxml')

data = {'Article Link': [], 'Article Heading': [], 'Image Link': [], 'Full News': []}

for article in soup.find_all('div', class_='iN5CR'):
    article_link = article.a['href']

    if article_link.startswith("https://timesofindia.indiatimes.com/india"):
        try:
            r2 = requests.get(article_link).text
            soup2 = BeautifulSoup(r2, 'lxml')
            article_heading = soup2.h1.text
            full_news = soup2.find('div', {'data-articlebody': '1'}).get_text()

            image_div = soup2.find('div', class_='wJnIp')
            if image_div and image_div.img:
                image_link = image_div.img['src']
            else:
                image_link = ""

            data['Article Link'].append(article_link)
            data['Article Heading'].append(article_heading)
            data['Image Link'].append(image_link)
            data['Full News'].append(full_news)
        except Exception as e:
            print(e)

df = pd.DataFrame(data)

# Save the data to an Excel file
df.to_excel('news_data.xlsx', index=False)
