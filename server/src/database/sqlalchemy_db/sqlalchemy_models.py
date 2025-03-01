import uuid

from flask_sqlalchemy import SQLAlchemy
import enum

from sqlalchemy import Enum, Date

db = SQLAlchemy()


class ClassificationType(enum.Enum):
    travel_tip = "travel_tip"
    travel_suggestion = "travel_suggestion"
    other = "other"


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    num_comments = db.Column(db.Integer, nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Text, primary_key=True)
    post_id = db.Column(db.Text, db.ForeignKey("posts.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    classification = db.Column(Enum(ClassificationType), nullable=False)
    start_date = db.Column(Date, nullable=True)
    end_date = db.Column(Date, nullable=True)
    characteristic = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)

    locations = db.relationship(
        "Location", backref="comment", cascade="all, delete-orphan"
    )


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    comment_id = db.Column(db.Text, db.ForeignKey("comments.id", ondelete="CASCADE"))
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    location_name = db.Column(db.Text, nullable=False)
    characteristic = db.Column(db.Text, nullable=False)
