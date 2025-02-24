import json

from handlers.base_ai_handler import BaseAIHandler


class ClassifySuggestionOrTipHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        prompt = f"""
        Please classify the following list of comments into one of the following categories:
        - "travel_suggestion" if it mentions a location you can visit.
        - "travel_tip" if it mentions travel hacks, tips, or advice.
        - "other" if it does not mention any of the above.

        Additionally provide a characteristic describing what the comment is related to (e.g. is it safety, transport, etc.?)
        Respond by giving a json object with the comment id as the key and classification and characteristic values contained within.
        stripped of any ```json``` or trailing and leading quotes.

        Comments:
        {input_data}
        """
        query_result = self.query_and_load_json(prompt)
        json_input_data = json.loads(input_data)
        for comment in json_input_data["comments"]:
            result_dict = query_result[comment["id"]]
            comment["classification"] = result_dict["classification"]
            comment["characteristic"] = result_dict["characteristic"]
        return json.dumps(json_input_data)
