import json

from handlers.base_ai_handler import BaseAIHandler

class SummarisePostsHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        prompt = f"""
        Summarise this objectively for the purpose of displaying travel tips and suggestions for users of an app. 
        Remove any references to people,users or personal experiences present. 
        Respond by giving a json object with the comment id as the key and the summarised text as the value, 
        stripped of any ```json``` or trailing and leading quotes.

        Comments:
        {input_data}
        """

        query_result = self.query_and_load_json(prompt)
        json_input_data = json.loads(input_data)
        for comment in json_input_data["comments"]:
            comment["summary"] = query_result.get(comment["id"])
        return json.dumps(json_input_data)