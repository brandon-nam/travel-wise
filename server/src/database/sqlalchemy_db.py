from flask import Response, jsonify

from src.database.base import BaseDB
from src.database.sql_models import Post, Comment, db


class SQLAlchemyDB(BaseDB):
    def setup_db(self) -> None:
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.db_connection_uri
        db.init_app(self.app)

    def get_posts(self) -> Response:
        posts = Post.query.all()
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
        comments = Comment.query.all()
        return jsonify(
            [
                {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "body": comment.body,
                    "karma": comment.karma,
                }
                for comment in comments
            ]
        )
