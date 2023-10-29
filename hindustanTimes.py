import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize a list to store the data
data = []

agent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
r = requests.get("https://www.hindustantimes.com/latest-news", headers=agent)

soup = BeautifulSoup(r.text, 'lxml')

filtered_elements = soup.find_all("h3", class_="hdg3")

for element in filtered_elements:
    try:
        article_title = element.a.text
        article_url = "https://www.hindustantimes.com" + element.a['href']

        r2 = requests.get(article_url, headers=agent)
        soup2 = BeautifulSoup(r2.text, 'lxml')

        # Initialize image_link as an empty string
        image_link = ""

        # Try to fetch the image_link, and handle exceptions
        try:
            image_link += soup2.find('div', class_='storyParagraphFigure').picture.source['srcset']
        except (AttributeError, KeyError) as e:
            print("Image not found:", e)

        full_news = ""
        story_details = soup2.find('div', class_='storyDetails')

        if story_details:
            for news in story_details.find_all('p'):
                full_news += news.text + "\n"
        else:
            full_news = "Story details not found."

        data.append({
            'Article Link': article_url,
            'Article Heading': article_title,
            'Image Link': image_link,
            'Full News': full_news
        })

    except Exception as e:
        print("An error occurred:", e)

df = pd.DataFrame(data)

df.to_excel('hindustantimes_data.xlsx', index=False)
