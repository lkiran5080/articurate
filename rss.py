import random

import feedparser


def get_links(feed_urls):
    links = []
    for feed_url in feed_url:
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            links.append(entry.link)
    if len(links) > 20:
        links = random.choices(links, k = 20)
    return links

if __name__ == '__main__':
    FEED_URL = "https://www.theguardian.com/uk/rss"

    FEED_URL = "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms"

    a = feedparser.parse(FEED_URL)

    urls = []
    for entry in a.entries:
        urls.append(entry.link)
        
    from pprint import pprint

    pprint(urls)

    print('len: ', len(urls))

    

    urls = random.choices(urls, k=20)

    print('rnd len: ', len(urls))

    pprint(urls)
