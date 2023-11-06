import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsArticle, NewsSource  # Import your NewsArticle and NewsSource models
from django.utils import timezone

class Command(BaseCommand):
    help = 'Scrape articles from source 4 and store them in the database'

    def handle(self, *args, **options):
        # Define the URL of source 4
        url = 'https://www.hindustantimes.com/latest-news'

        try:
            agent = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
            }

            r = requests.get(url, headers=agent)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find or create the NewsSource object
            source_name = "Hindustan Times"  # Change this to match the actual source name
            source_url = url
            news_source, created = NewsSource.objects.get_or_create(name=source_name, url=source_url)

            filtered_elements = soup.find_all("h3", class_="hdg3")

            for element in filtered_elements:
                try:
                    article_title = element.a.text
                    article_url = "https://www.hindustantimes.com" + element.a['href']

                    r2 = requests.get(article_url, headers=agent)
                    soup2 = BeautifulSoup(r2.text, 'lxml')

                    # Initialize image_link as an empty string
                    image_link = ""

                    # Try to fetch the image_link and handle exceptions
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

                    # Create or update the NewsArticle object
                    article_obj, created = NewsArticle.objects.get_or_create(
                        article_link=article_url,
                        defaults={
                            'title': article_title,
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
