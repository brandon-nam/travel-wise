import json

from handlers.base_ai_handler import BaseAIHandler


class ClassifyLocationCoordinatesHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        prompt = f"""
        For each location mentioned in these comments, identify their respective coordinates.
        
        Comments:{input_data}
        
        Respond with a json object where the comment_id is the key and a list of dictionaries as values, where each dictionary contains:
        `"lat"` (latitude, float)
        `"lng"` (longitude, float)
        `"location_name"` (location_name, string, i.e. what is the name of the location?)
        `"characteristic"` (characteristic, string, i.e. what kind of location is it? e.g. city, theme park, place of worship, restaurant, etc.)
        .
        If there are multiple locations, provide the information for all of them. 
        If there are no identifiable locations mentioned, return an empty list instead.

        {{
          "mbomop8": [
            {{"lat": 35.3192, "lng": 139.5467, "location_name": "Tokyo", "characteristic": "city"}}, 
            {{"lat": 35.4449, "lng": 139.6368, "location_name": "Universal Studios Japan", "characteristic": "theme park"}}
          ],
          "mbr1lyf": [
            {{"lat": 35.7719, "lng": 140.3929, "location_name": "Wagyu Idaten", "characteristic": "restaurant"}}, 
            {{"lat": 35.0116, "lng": 135.7681, "location_name": "Ghibli Museum", "characteristic": "museum"}}
          ],
          "mba3rta": [],
        }}
        
        Do not return any other text, and make sure the response is stripped of any ```json``` or trailing and leading quotes.
        
        I will call json.loads() on what you provide as a response, and it should work.

        """
        query_result = self.query_and_load_json(prompt)
        json_input_data = json.loads(input_data)
        for comment in json_input_data["comments"]:
            comment["locations"] = query_result.get(comment["id"])
        return json.dumps(json_input_data)
