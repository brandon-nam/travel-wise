import json

from src.handlers.base_ai_handler import BaseAIHandler


class SummarisePostsHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        prompt = f"""
        Summarize this for the purpose of providing useful travel tips and suggestions.
            - If the comment is a question, answer it concisely based on general knowledge.
            - Remove references to users, personal experiences, and opinions.
            - Provide objective travel-related information.
            - If the comment only mentions a place, item name or object, state what it is and why it might be useful for travelers.
            Respond by giving a json object with the comment id as the key and the summarised text as the value, 
            stripped of any ```json``` or trailing and leading quotes.
            Ensure a summary is generated for every comment.

        Comments:
        {input_data}
        """

        query_result = self.query_and_load_json(prompt)
        json_input_data = json.loads(input_data)
        for comment in json_input_data["comments"]:
            comment["summary"] = query_result.get(comment["id"], "")
        return json.dumps(json_input_data)
