import os
import random
import uuid
from pprint import pprint

import newspaper
import pyttsx3
from flask import (Blueprint, current_app, jsonify, render_template, request,
                   send_from_directory)
from flask_login import current_user, login_required

from app import db
from app.articurate import (clean_text_for_audio, clean_text_for_summary,
                            declutter, extract, extract_with_metadata, gen_fn,
                            summarize, synthesize)
from app.models import Entry, Feed, User

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/link", methods=["GET", "POST"])
def get_link():

    if request.method == "POST":
        request_data = request.json
        source_url = request_data["source_url"]

        # A new article entry
        entry = Entry()
        entry.source_url = source_url
        # entry.user_id = current_user.id

        data = extract_with_metadata(source_url)

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

        response_data = {
            "source_url": source_url,
            "title": title,
            "publish_date": publish_date,
            "authors": authors,
            "top_image": top_image,
            "summary": summary,
            "audio_file": new_fn,
            "content": decluttered_text,
        }

        return jsonify(response_data), 200

    return render_template("link.html")


@main.route("/text")
def get_text():
    return render_template("text.html")


@main.route("/articurate", methods=["POST"])
def get_articurate():

    request_data = request.json
    source_url = request_data["source_url"]

    # A new article entry
    entry = Entry()
    entry.source_url = source_url
    # entry.user_id = current_user.id

    data = extract_with_metadata(source_url)

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

    response_data = {
        "source_url": source_url,
        "title": title,
        "publish_date": publish_date,
        "authors": authors,
        "top_image": top_image,
        "summary": summary,
        "audio_file": new_fn,
        "content": decluttered_text,
    }

    return jsonify(response_data), 200


@main.route("/listen/<filename>")
def get_audio(filename):
    dir_path = os.path.join("data", "audio")
    return send_from_directory(directory=dir_path, path=filename)


@main.route("/feed")
def get_latest_feed():

    # get the latest generated feed from database https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
    feed = Feed.query.order_by(Feed.feed_generated.desc()).first()

    # query all article entries with feed id as foreign id
    feed_entries = feed.entries.all()

    # jumble the feed list
    random.shuffle(feed_entries)

    # pprint(feed_entries)

    return render_template("feed.html", feed_entries=feed_entries)


@main.route("/feed/<feed_id>")
def get_feed(feed_id):
    feed = Feed.query.get(feed_id)
    feed_entries = feed.entries.all()
    random.shuffle(feed_entries)

    # pprint(feed_entries)

    return render_template("feed.html", feed_entries=feed_entries)


@main.route("/u/<username>")
def get_user(username):

    user = User.query.filter_by(username=username).first_or_404()

    user_entries = user.entries.all()

    return render_template("user.html", user_entries=user_entries)


@main.route("/e/<entry_id>")
def get_entry(entry_id):

    entry = Entry.query.get_or_404(entry_id)

    return render_template("entry.html", entry=entry)
