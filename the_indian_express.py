import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize a list to store the data
data = []

r = requests.get("https://indianexpress.com")
soup = BeautifulSoup(r.text, 'lxml')

filtered_elements = soup.find_all(class_=lambda value: value and "other-article" in value)

for element in filtered_elements:
    try:
        if "m-premium" in element["class"]:
            continue
        article_heading = element.h3.a.text
        article_link = element.h3.a['href']

        r2 = requests.get(article_link)
        soup2 = BeautifulSoup(r2.text, 'lxml')
        image_element = soup2.find('span', class_='custom-caption')

        if image_element and image_element.img:
            image_link = image_element.img['src']
        else:
            image_link = ""

        full_news = ""
        for news in soup2.find('div', class_='story_details').find_all('p'):
            full_news += news.text + "\n"

        data.append({
            'Article Link': article_link,
            'Article Heading': article_heading,
            'Image Link': image_link,
            'Full News': full_news
        })
    except Exception as e:
        print("An error occurred:", e)


filtered_elements = soup.find('div', class_="top-news").ul.find_all('li')

for element in filtered_elements:
    try:
        article_heading = element.h3.a.text
        article_link = element.h3.a['href']
        print(article_link)
        print(article_heading)

        r2 = requests.get(article_link)
        soup2 = BeautifulSoup(r2.text, 'lxml')
        image_element = soup2.find('span', class_='custom-caption')

        if image_element and image_element.img:
            image_link = image_element.img['src']
        else:
            image_link = ""

        full_news = ""
        for news in soup2.find('div', class_='story_details').find_all('p'):
            full_news += news.text + "\n"

        data.append({
            'Article Link': article_link,
            'Article Heading': article_heading,
            'Image Link': image_link,
            'Full News': full_news
        })
    except Exception as e:
        print("An error occurred:", e)




# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Save the data to an Excel file
df.to_excel('news_data.xlsx', index=False)
