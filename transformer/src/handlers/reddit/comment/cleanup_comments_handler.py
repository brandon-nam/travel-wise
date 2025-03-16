import json
import re

from src.handlers.base_handler import BaseHandler


def clean_string(s: str) -> str:
    s = re.sub(r"\\u[0-9A-Fa-f]{4}", "", s)
    s = re.sub(r"\\[nrt]", " ", s)
    s = s.replace("\xa0", " ")
    s = s.strip()
    return s


class CleanupCommentsHandler(BaseHandler):
    def do_handle(self, input_data: str) -> str:
        json_data = json.loads(input_data)

        for comment in json_data:
            if len(comment["body"]) > 200:
                comment["body"] = comment["body"][:200]
            comment["body"] = clean_string(comment["body"])
        return json.dumps(json_data, indent=4)
