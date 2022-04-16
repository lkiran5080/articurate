import os
import uuid

from flask import current_app
from newspaper import Article

from app import create_app, db
from app.articurate import (clean_text_for_audio, clean_text_for_summary,
                            declutter, extract, extract_with_metadata, gen_fn,
                            summarize, synthesize)
from app.models import Entry, Feed

app = create_app()

def gen_feed_from_urls(urls):

    feed = Feed()

    db.session.add(feed)
    db.session.commit()

    feed_id = feed.id

    for url in urls:
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
        per = 0.1
        summary = summarize(text_for_summary, per=per)
        entry.summary = summary
        
        # Synthesize
        new_fn = gen_fn() 
        path = os.path.join(current_app.root_path, "data", "audio", new_fn)
        synthesize(text_for_audio, path)
        entry.audio_file = new_fn

        # Commit entry to database
        db.session.add(entry)
        db.session.commit()
        
    return feed_id
        
        
if __name__ == '__main__':
    
    sample_feed_urls = ["https://www.technologyreview.com/2020/11/06/1011726/ai-natural-language-processing-computer-vision/","https://hbr.org/2022/04/the-state-of-globalization-in-2022"]
    
    sample2 = ['https://www.theguardian.com/politics/2022/apr/15/tory-mp-steve-baker-shares-paper-denying-climate-crisis',
    'https://www.theguardian.com/uk-news/video/2021/mar/19/made-in-doncaster-i-am-not-your-subject-video',
    'https://www.theguardian.com/environment/2022/apr/15/beginners-guide-to-planting-trees-and-fighting-climate-crisis',
    'https://www.theguardian.com/news/audio/2022/apr/15/where-did-it-all-go-wrong-for-imran-khan-podcast',
    'https://www.theguardian.com/sport/2022/apr/14/emma-raducanu-clay-debut-billie-jean-king-cup-great-brtiain',
    'https://www.theguardian.com/world/2022/apr/15/bank-of-england-owned-599-slaves-in-1770s-new-exhibition-reveals',
    'https://www.theguardian.com/world/2022/apr/15/paella-spain-top-chefs-space-food-michelin-commerical-travel',
    'https://www.theguardian.com/world/2022/apr/15/emmanuel-macron-wants-cap-on-executive-pay-france',   
    'https://www.theguardian.com/artanddesign/gallery/2022/apr/14/the-personal-touch-this-years-portrait-of-humanity-prize-winners-in-pictures',
    'https://www.theguardian.com/commentisfree/2022/apr/15/easter-beats-christmas-spring-passover-ramadan',
    'https://www.theguardian.com/sport/2022/apr/14/emma-raducanu-clay-debut-billie-jean-king-cup-great-brtiain',
    'https://www.theguardian.com/feasting-with-ocado/2022/apr/08/rukmini-iyers-recipe-for-slow-cooked-lamb-leg-al-pastor-with-pineapple-salsa',
    'https://www.theguardian.com/info/ng-interactive/2021/oct/20/sign-up-for-down-to-earth-the-best-way-to-make-sense-of-the-biggest-environment-stories',
    'https://www.theguardian.com/world/video/2022/apr/14/inside-ukraines-suburban-horror-i-have-nothing-left-video',
    'https://www.theguardian.com/football/2022/mar/22/sign-up-for-our-new-womens-football-newsletter-moving-the-goalposts',
    'https://www.theguardian.com/football/2022/apr/15/manchester-united-fans-hold-anti-glazer-protest-at-training-ground',
    'https://www.theguardian.com/commentisfree/2022/apr/15/rape-weapon-ukraine-war-crime-sexual-violence',
    'https://www.theguardian.com/us-news/2022/apr/15/us-capitol-rioter-blames-trump-actions-found-guilty',
    'https://www.theguardian.com/sport/2022/apr/15/youre-only-as-good-as-your-players-darren-gough-defends-joe-roots-record',
    'https://www.theguardian.com/artanddesign/gallery/2022/apr/14/the-personal-touch-this-years-portrait-of-humanity-prize-winners-in-pictures']
    
    sample3 = ['https://timesofindia.indiatimes.com/gadgets-news/windows-11-users-may-soon-get-support-for-third-party-widgets/articleshow/90863557.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/oneplus-reveals-another-big-specification-of-the-oneplus-10r-smartphone-set-to-launch-on-april-28/articleshow/90863481.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/exclusive-galaxy-m53-5g-samsungs-most-powerful-m-series-smartphone-to-launch-in-india-soon/articleshow/90858654.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/oppo-f21-pro-goes-on-sale-india-price-specs-and-offers/articleshow/90857757.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/future-apple-iphones-may-get-this-new-camera-lens/articleshow/90849462.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/exclusive-galaxy-m53-5g-samsungs-most-powerful-m-series-smartphone-to-launch-in-india-soon/articleshow/90858654.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/why-windows-users-can-skip-the-april-2022-update-from-microsoft/articleshow/90847766.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/exclusive-galaxy-m53-5g-samsungs-most-powerful-m-series-smartphone-to-launch-in-india-soon/articleshow/90858654.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/wordle-300-answer-for-april-15-2022/articleshow/90858157.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/iqoo-to-launch-z6-pro-5g-in-india-soon-launch-date-expected-price-and-more/articleshow/90853146.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/oneplus-reveals-another-big-specification-of-the-oneplus-10r-smartphone-set-to-launch-on-april-28/articleshow/90863481.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/explained-audio-quality-via-smartphones-and-does-wired-connection-offer-better-audio-quality/articleshow/90847483.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/windows-11-users-may-soon-get-support-for-third-party-widgets/articleshow/90863557.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/wordle-300-answer-for-april-15-2022/articleshow/90858157.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/explained-what-is-google-arcore-and-how-is-it-useful/articleshow/90850478.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/oneplus-reveals-another-big-specification-of-the-oneplus-10r-smartphone-set-to-launch-on-april-28/articleshow/90863481.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/infinix-hot-11-2022-with-5000mah-battery-launched-priced-at-rs-8999/articleshow/90863604.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/poco-f4-gt-is-set-to-launch-on-april-27/articleshow/90853119.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/iqoo-neo-6-smartphone-launched-price-and-specifications/articleshow/90850040.cms',
 'https://timesofindia.indiatimes.com/gadgets-news/why-windows-users-can-skip-the-april-2022-update-from-microsoft/articleshow/90847766.cms']
    
    """ with app.app_context():
        feed_id = gen_feed_from_urls(sample_feed_urls) """
        
    sample4 = ["https://hbr.org/2022/04/supporting-employee-caregivers-starts-with-better-data","https://hbr.org/2022/04/the-state-of-globalization-in-2022", "https://www.technologyreview.com/2020/11/06/1011726/ai-natural-language-processing-computer-vision/"]
        
    with app.app_context():
        feed_id = gen_feed_from_urls(sample4)
