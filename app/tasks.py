from app.models import Article
from flask_login import current_user
import newspaper


def articurate(url):

    # TODO: create a new Articles entry
    # TODO: save source_url
    article_entry = Article(source_url=url, user_id=current_user.id)

    # TODO: download and parse the article
    # TODO: save metadata and content
    article = newspaper.Article(url)
    article.download()
    article.parse()

    content = article.text
    article_entry.content = content

    # TODO: summarize contents

    # TODO: save contents to db

    # TODO: generate audi file and save
    # TODO: add audio_file path to db

    # TODO: commit to db

    # TODO: return results; summary, contents, metadata, audio_file

    pass
