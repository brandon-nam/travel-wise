from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    karma = db.Column(db.Integer, nullable=False)
    num_comments = db.Column(db.Integer, nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Text, primary_key=True)
    post_id = db.Column(db.Text, db.ForeignKey("posts.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    karma = db.Column(db.Integer, nullable=False)
