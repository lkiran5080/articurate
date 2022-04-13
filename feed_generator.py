from app import db
from app.models import Feed, Article


def gen_feed_from_urls(urls):

    feed = Feed()

    db.session.add(feed)
    db.session.commit()

    feed_id = feed.id

    for url in urls:
        article_entry = Article(feed_id=feed_id)

        # add data to entry

    # TODO
    pass
