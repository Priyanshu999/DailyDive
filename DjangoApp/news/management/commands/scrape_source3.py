import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsArticle, NewsSource  # Import your NewsArticle and NewsSource models
from django.utils import timezone

class Command(BaseCommand):
    help = 'Scrape articles from source 3 and store them in the database'

    def handle(self, *args, **options):
        # Define the URL of source 3
        url = 'https://indianexpress.com'

        try:
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find or create the NewsSource object
            source_name = "Indian Express"  # Change this to match the actual source name
            source_url = url
            news_source, created = NewsSource.objects.get_or_create(name=source_name, url=source_url)

            filtered_elements = soup.find_all(class_=lambda value: value and "other-article" in value)

            for element in filtered_elements:
                try:
                    if "m-premium" in element["class"]:
                        continue
                    article_heading = element.h3.a.text
                    article_link = element.h3.a['href']

                    r2 = requests.get(article_link)
                    soup2 = BeautifulSoup(r2.text, 'html.parser')

                    # Initialize image_link as an empty string
                    image_link = ""

                    # Try to fetch the image_link and handle exceptions
                    try:
                        image_element = soup2.find('span', class_='custom-caption')
                        if image_element and image_element.img:
                            image_link = image_element.img['src']
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

                    # Create or update the NewsArticle object
                    article_obj, created = NewsArticle.objects.get_or_create(
                        article_link=article_link,
                        defaults={
                            'title': article_heading,
                            'content': full_news,
                            'image_url': image_link,
                            'source': news_source,
                            'publication_date': timezone.now(),
                        }
                    )

                    if not created:
                        # Article already exists, break from the loop
                        self.stdout.write(self.style.NOTICE(f'Article already exists: {article_obj.title}'))
                        break
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Successfully scraped: {article_obj.title}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error scraping an article: {e}'))

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching the source: {e}'))

        self.stdout.write(self.style.SUCCESS('Scraping completed'))
