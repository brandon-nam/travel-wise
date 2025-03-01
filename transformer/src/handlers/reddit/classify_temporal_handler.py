import json

from src.handlers.base_ai_handler import BaseAIHandler


class ClassifyTemporalHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        prompt = f"""
            Identify a date range with a start and end date from these comments:
            
            Comments: {input_data}
            
            If an exact date is mentioned, return that date as both the start and end dates.
            If a specific date range is mentioned, return the respective start date and end date.
            If a season is mentioned, approximate a two-week date range and return the respective start date and end date.
            If no dates are found, return null for both.
    
            Return a json object with the following structure where the comment_id is the key and the dictionary is the value, for example:
            {{
              "mbomop8": {{"start_date": YYYY-MM-DD | None, "end_date": YYYY-MM-DD | None}}
            }}
    
            Do not return any other text, and make sure the response is stripped of any ```json``` or trailing and leading quotes.
            
            I will call json.loads() on what you provide as a response, and it should work.
            

            """

        query_result = self.query_and_load_json(prompt)
        json_input_data = json.loads(input_data)
        for comment in json_input_data["comments"]:
            date_dict = query_result.get(comment["id"])
            comment["start_date"] = date_dict["start_date"]
            comment["end_date"] = date_dict["end_date"]
        return json.dumps(json_input_data)
