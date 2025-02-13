from flask import Response, jsonify, Flask
from sqlalchemy.orm import joinedload

from src.database.base_db import BaseDB
from src.database.sqlalchemy_db.sqlalchemy_models import Post, Comment, db


class SQLAlchemyDB(BaseDB):
    def setup_db(self, app: Flask) -> None:
        app.config["SQLALCHEMY_DATABASE_URI"] = self.db_connection_uri
        db.init_app(app)

    def get_posts(self) -> Response:
        posts = db.session.query(Post).all()
        return jsonify(
            [
                {
                    "id": post.id,
                    "title": post.title,
                    "url": post.url,
                    "karma": post.karma,
                    "num_comments": post.num_comments,
                }
                for post in posts
            ]
        )

    def get_comments(self) -> Response:
        comments = (
            db.session.query(Comment).options(joinedload(Comment.locations)).all()
        )
        return jsonify(
            [
                {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "body": comment.body,
                    "karma": comment.karma,
                    "classification": comment.classification.value,
                    "start_date": comment.start_date,
                    "end_date": comment.end_date,
                    "location_coordinates": [
                        {"lat": loc.lat, "lng": loc.lng} for loc in comment.locations
                    ],
                }
                for comment in comments
            ]
        )
