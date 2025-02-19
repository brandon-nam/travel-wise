import json
from collections import defaultdict

from handlers.base_handler import BaseHandler


class SplitPostsAndCommentsHandler(BaseHandler):
    def do_handle(self, input_data: str) -> str:
        json_data = json.loads(input_data)
        result = defaultdict(list)
        for entry in json_data:
            post = {
                "title": entry["title"],
                "id": entry["id"],
                "url": entry["url"],
                "score": entry["score"],
            }
            result["posts"].append(post)
            result["comments"].extend(entry["comments"])
        return json.dumps(result, indent=4)
