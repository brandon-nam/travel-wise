from flask import jsonify, Response

from src.database.sql_models import Comment, Post


def create_routes(app) -> None:
    @app.route("/posts", methods=["GET"])
    def get_posts() -> Response:
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

    @app.route("/comments", methods=["GET"])
    def get_comments() -> Response:
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
