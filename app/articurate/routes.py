import os
import uuid
from pprint import pprint

import newspaper
import pyttsx3
from app import db
from app.models import Article, Feed
from flask import (Blueprint, jsonify, render_template, request,
                   send_from_directory, current_app)
from flask_login import current_user, login_required

articurate = Blueprint('articurate', __name__)


@articurate.route('/')
def index():
    return "Server Up!"


@articurate.route('/link')
def get_home():
    return render_template('link.html')


@articurate.route('/text')
def get_home():
    return render_template('text.html')


@articurate.route("/articurate", methods=['POST'])
def get_articurate():

    request_data = request.json
    source_url = request_data['source_url']

    # A new article entry
    article_entry = Article()
    article_entry.source_url = source_url
    #article_entry.user_id = current_user.id

    # Download the article
    article = newspaper.Article(source_url)
    article.download()

    # Parse the article
    article.parse()
    # metada
    title = article.title
    publish_date = article.publish_date
    authors = article.authors

    stringified_authors = ""
    for author in authors:
        stringified_authors += f'{author};'

    # extracted content
    content = article.text
    # media
    top_image = article.top_image
    images = article.images
    movies = article.movies

    # Metadata entry
    article_entry.title = title
    article_entry.publish_date = publish_date
    #article_entry.authors = authors
    article_entry.authors = stringified_authors

    # Extracted Content entry
    article_entry.content = content

    # Media Files
    article_entry.top_image = top_image
    # not storing images, movies as it is a list
    #article_entry.images = images
    #article_entry.movies = movies

    # summarize
    article.nlp()
    summary = article.summary
    article_entry.summary = summary
    # light weight : works well

    # transformers

    # tts
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    new_filename = str(uuid.uuid4()) + '.mp3'

    file_path = os.path.join(current_app.root_path,
                             'data', 'audio', new_filename)
    #file_path = f'data//audio//{new_filename}'

    print(file_path)

    # engine.say(content)
    #engine.save_to_file(content, new_filename)
    engine.save_to_file(content, file_path)
    engine.runAndWait()

    article_entry.audio_file = new_filename

    db.session.add(article_entry)
    db.session.commit()

    response_data = {
        "summary": summary,
        "content": content,
        "audio_file": new_filename,
        "title": title,
        "publish_date": publish_date,
        "authors": stringified_authors,
        "source_url": source_url
    }

    pprint(response_data)

    return jsonify(response_data), 200


@articurate.route("/listen/<filename>")
def get_audio(filename):
    dir_path = os.path.join('data', 'audio')
    return send_from_directory(directory=dir_path, path=filename)


@articurate.route("/feed")
def get_feed():

    # get the latest generated feed from database https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
    feed = Feed.query.order_by(Feed.feed_generated.desc()).first()

    # query all articles with feed id as foreign id
    feed_articles = feed.articles

    return render_template('feed.html', feed_articles=feed_articles)
