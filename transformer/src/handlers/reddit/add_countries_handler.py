import json

from src.handlers.base_ai_handler import BaseAIHandler


class AddCountriesHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        # prompt for adding countries
        prompt = f"""
        {input_data}
        """
        # query_result = self.query_and_load_json(prompt)
        
        json_input_data = json.loads(input_data)
        for post in json_input_data["posts"]:
            # result_dict = query_result[comment["id"]]
            # post["country"] = result_dict["country"]
            post["country"] = "japan"
            
        return json.dumps(json_input_data)
