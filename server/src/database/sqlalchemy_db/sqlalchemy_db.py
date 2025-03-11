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
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "country": post.country,
                }
                for post in posts
            ]
        )

    def get_comments(self, classification: str = "", country: str = "") -> Response:
        query = db.session.query(Comment).options(joinedload(Comment.locations))

        if classification in ("travel-suggestion", "travel-tip", "other"):
            classification = classification.replace("-", "_")
            query = query.filter(Comment.classification == classification)

        if country in ("japan", "korea"):
            query = query.join(Post, Comment.post_id == Post.id).filter(
                Post.country == country
            )

        comments = query.all()
        return jsonify(
            [
                {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "body": comment.body,
                    "score": comment.score,
                    "classification": comment.classification.value,
                    "start_date": comment.start_date,
                    "end_date": comment.end_date,
                    "characteristic": comment.characteristic,
                    "summary": comment.summary,
                    "location_coordinates": [
                        {
                            "lat": loc.lat,
                            "lng": loc.lng,
                            "location_name": loc.location_name,
                            "characteristic": loc.characteristic,
                        }
                        for loc in comment.locations
                    ],
                }
                for comment in comments
            ]
        )
