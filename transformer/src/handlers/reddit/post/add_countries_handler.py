import json
import re

from src.handlers.base_handler import BaseHandler


def extract_subreddit(url: str) -> str:
    match = re.search(r"reddit\.com/r/([^/]+)/", url)
    return match.group(1) if match else ""


class AddCountriesHandler(BaseHandler):
    def do_handle(self, input_data: str) -> str:
        json_input_data = json.loads(input_data)
        for post in json_input_data:
            subreddit = extract_subreddit(post["url"]).lower()
            if "japan" in subreddit:
                post["country"] = "japan"
            elif "korea" in subreddit:
                post["country"] = "korea"
            else:
                post["country"] = "unknown"

        return json.dumps(json_input_data)
