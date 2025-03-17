import os

from database.sqlalchemy.models import Comment, Post, Location, metadata
from database.sqlalchemy.repository import Repository
from flask import Response, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import joinedload


db = SQLAlchemy(metadata=metadata)


class ServerRepository(Repository):
    def __init__(self):
        super().__init__(db.session)

    def setup_db(self, app: Flask) -> None:
        db_host, db_port, db_user, db_password, db_name, db_driver = (
            os.getenv("DB_HOST") or "localhost",
            os.getenv("DB_PORT") or "5432",
            os.getenv("DB_USER") or "postgres",
            os.getenv("DB_PASSWORD") or "",
            os.getenv("DB_NAME") or "travelwise",
            os.getenv("DB_DRIVER") or "postgresql",
        )

        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        db.init_app(app)

    def get_posts(self) -> Response:
        posts = self.get_all(Post)
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
        query = self.session.query(Comment).options(joinedload(Comment.locations))

        if classification in ("travel-suggestion", "travel-tip", "other"):
            classification = classification.replace("-", "_")
            query = query.filter(Comment.classification == classification)

        if country in ("japan", "korea"):
            query = query.join(Post, Comment.post_id == Post.id).filter(
                func.lower(Post.country) == country.lower()
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
                    "post_url": comment.post.url,
                }
                for comment in comments
            ]
        )

    def get_countries(self) -> Response:
        countries = self.session.query(Post.country).distinct().all()
        return jsonify([country[0] for country in countries])

    def get_characteristics(self, classification: str = "") -> Response:
        query = self.session.query(Location.characteristic)

        if classification in ("travel-suggestion", "travel-tip", "other"):
            classification = classification.replace("-", "_")
            query = query.filter(Comment.classification == classification)

        characteristics = query.distinct().all()

        return jsonify([characteristic[0] for characteristic in characteristics])

    def get_locations_characteristics(self) -> Response:
        query = self.session.query(Location.characteristic)

        characteristics = query.distinct().all()

        return jsonify([characteristic[0] for characteristic in characteristics])
