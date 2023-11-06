import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsArticle, NewsSource
from django.utils import timezone

class Command(BaseCommand):
    help = 'Scrape articles from source 1 and store them in the database'

    def handle(self, *args, **options):
        # Define the URL of source 1
        url = 'https://timesofindia.indiatimes.com/india'

        # Perform the web scraping
        try:
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')

            # Create or get the NewsSource object
            source_name = "Times of India"  # You can change this to your desired source name
            source, created = NewsSource.objects.get_or_create(name=source_name, url=url)

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

                        # Create or update the NewsArticle object
                        article_obj, created = NewsArticle.objects.get_or_create(
                            article_link=article_link,
                            defaults={
                                'title': article_heading,
                                'content': full_news,
                                'image_url': image_link,
                                'source': source,
                                'publication_date': timezone.now(),
                            }
                        )

                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Successfully scraped: {article_obj.title}'))
                        else:
                            self.stdout.write(self.style.NOTICE(f'Article already exists: {article_obj.title}'))
                            break

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping an article: {e}'))

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching the source: {e}'))

        self.stdout.write(self.style.SUCCESS('Scraping completed'))
