import random
from pprint import pprint

import feedparser

FEED_URL = "https://www.theguardian.com/uk/rss"

FEED_URL = "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms"

a = feedparser.parse(FEED_URL)

urls = []
for entry in a.entries:
    urls.append(entry.link)


pprint(urls)

print("len: ", len(urls))


urls = random.choices(urls, k=20)

print("rnd len: ", len(urls))

pprint(urls)
