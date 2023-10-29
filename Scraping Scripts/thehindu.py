import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize a list to store the data
data = []

r = requests.get("https://www.thehindu.com/latest-news/")
soup = BeautifulSoup(r.text, 'lxml')

filtered_elements = soup.find('div', class_=lambda value: value and "latest-news" in value).find_all('div', class_='element')

for element in filtered_elements:
    try:
        article_heading = element.find('h3', class_='title').a.text
        article_link = element.find('h3', class_='title').a['href']

        r2 = requests.get(article_link)
        soup2 = BeautifulSoup(r2.text, 'lxml')

        # Initialize image_link as an empty string
        image_link = ""

        # Try to fetch the image_link, and handle exceptions
        try:
            image_link += soup2.find('picture').source['srcset']
        except (AttributeError, KeyError) as e:
            print("Image not found:", e)

        full_news = ""
        article_body = soup2.find('div', class_=lambda value: value and "articlebodycontent" in value)

        if article_body:
            for news in article_body.find_all('p'):
                full_news += news.text + "\n"
            full_news = full_news.split("COMMents")[0]
        else:
            full_news = "Article body not found."

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
df.to_excel('news_data_thehindu.xlsx', index=False)
