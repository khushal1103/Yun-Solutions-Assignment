import feedparser
import datetime
from newspaper import Article
import nltk
import sys

# Download necessary NLTK data
nltk.download('punkt')

def scrape_website(url):
    toi_article = Article(url, language="en")
    toi_article.download()  
    toi_article.parse()  
    toi_article.nlp()  
    return {'title': toi_article.title, 'text': toi_article.text, 'summary': toi_article.summary, 'keywords': toi_article.keywords}

def scrape_google_news_feed(query):
    rss_url = f'https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en'
    feed = feedparser.parse(rss_url)
    current_time = datetime.datetime.now()
    news = []
    if feed.entries:
        for entry in feed.entries:
            pubdate = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
            time_difference = current_time - pubdate
            if time_difference.total_seconds() <= 24 * 60 * 60:
                title = entry.title
                link = entry.link
                description = entry.description
                pubdate = entry.published
                source = entry.source
                try:
                    content = scrape_website(link)
                    news.append({'title': content['title'], 'summary': content['summary'], 'keywords': ",".join(content['keywords']), 'source': source})
                except:
                    news.append({'title': title, 'source': source})
    return news

def print_data(news):
    for x in news:
        for i in x.keys():
            print(i, "--", x[i])
            print()
        print()
        print()
        print()

# Check if a command-line argument is provided
if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    query = input("Enter your query: ")

news = scrape_google_news_feed(query)
print_data(news)
