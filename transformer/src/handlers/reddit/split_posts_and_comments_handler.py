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
                "num_comments": len(entry["comments"]),
            }
            result["posts"].append(post)
            for comment in entry["comments"]:
                comment["post_id"] = entry["id"]
            result["comments"].extend(entry["comments"])
        return json.dumps(result, indent=4)
