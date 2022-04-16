from datetime import datetime

from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    account_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(60), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)

    entries = db.relationship("Entry", backref="entry_author", lazy="dynamic")

    def __repr__(self) -> str:
        return f"User('{self.id}','{self.account_created}','{self.username}', '{self.email}')"


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    entry_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    source_url = db.Column(db.String(240))

    title = db.Column(db.String(100))
    published_date = db.Column(db.DateTime)
    authors = db.Column(db.String(240))

    top_image = db.Column(db.String(240))

    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    audio_file = db.Column(db.String(240))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    feed_id = db.Column(db.Integer, db.ForeignKey("feeds.id"))

    def __repr__(self) -> str:
        return f"Entry('{self.id}', '{self.entry_created}', '{self.source_url}')"


class Feed(db.Model):
    __tablename__ = "feeds"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    feed_generated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    entries = db.relationship("Entry", lazy="dynamic")

    def __repr__(self) -> str:
        return f"Feed('{self.id}', '{self.feed_generated}')"
