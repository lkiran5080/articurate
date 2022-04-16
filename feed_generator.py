import os
import random
import uuid

import feedparser
from flask import current_app
from newspaper import Article

from app import create_app, db
from app.articurate import (clean_text_for_audio, clean_text_for_summary,
                            declutter, extract, extract_with_metadata, gen_fn,
                            summarize, synthesize)
from app.models import Entry, Feed

app = create_app()

def get_links(feed_urls):
    links = []
    
    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            links.append(entry.link)
            
    if len(links) > 30:
        links = random.choices(links, k = 30)
    
    links = list(set(links))
    
    return links

def gen_feed_from_urls(urls):

    feed = Feed()

    db.session.add(feed)
    db.session.commit()

    feed_id = feed.id

    for url in urls:
        try:
            print(f"Processing url: {url} ...")
            entry = Entry(feed_id=feed_id)
            entry.source_url = url
            
            data = extract_with_metadata(url)
            
            # Metadata entry
            title = data["title"]
            publish_date = data["publish_date"]
            authors = data["authors"]
            top_image = data["top_image"]
            
            entry.title = title
            entry.publish_date = publish_date
            entry.authors = authors
            
            entry.top_image = top_image
            
            
            
            text = data["text"]
            
            # Declutter for web
            decluttered_text = declutter(text)
            entry.content = decluttered_text
            
            # prepare extracted text for models
            text_for_summary = clean_text_for_summary(text)
            text_for_audio = clean_text_for_audio(text)
            
            # Summarize
            
            summary = summarize(text_for_summary)
            entry.summary = summary
            
            # Synthesize
            new_fn = gen_fn() 
            path = os.path.join(current_app.root_path, "data", "audio", new_fn)
            synthesize(text_for_audio, path)
            entry.audio_file = new_fn

            # Commit entry to database
            db.session.add(entry)
            db.session.commit()
        except:
            pass
        
    return feed_id
        
        
if __name__ == '__main__':
  
    sample_feed_urls = ["https://hbr.org/2022/04/supporting-employee-caregivers-starts-with-better-data","https://hbr.org/2022/04/the-state-of-globalization-in-2022", "https://www.technologyreview.com/2020/11/06/1011726/ai-natural-language-processing-computer-vision/"]
    
    links = get_links(["http://feeds.hbr.org/harvardbusiness","https://news.mit.edu/rss/feed", "http://feeds.feedburner.com/scroll_in.rss"])
        
    with app.app_context():
        feed_id = gen_feed_from_urls(links)
        print(feed_id)
        
    
