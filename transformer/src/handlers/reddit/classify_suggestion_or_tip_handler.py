import json

from handlers.base_ai_handler import BaseAIHandler


class ClassifySuggestionOrTipHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        prompt = f"""
        Please classify the following list of comments into one of the following categories:
        - "travel_suggestion" if it mentions a location you can visit.
        - "travel_tip" if it mentions travel hacks, tips, or advice.
        - "other" if it does not mention any of the above.

        Respond by giving a json object with comment_id as key, and classification as value, 
        stripped of any ```json``` or trailing and leading quotes.

        Comments:
        {input_data}
        """
        query_result = self.query_and_load_json(prompt)
        json_input_data = json.loads(input_data)
        for comment in json_input_data["comments"]:
            classification = query_result[comment["id"]]
            comment["classification"] = classification
        return json.dumps(json_input_data)
