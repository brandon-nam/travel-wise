import json
from typing import Any

from src.handlers.base_handler import BaseHandler

THRESHOLD = 1000  # consider locations 1km apart to be the "same"


def distance(first_loc: dict[str, Any], second_loc: dict[str, Any]):
    lat1, lng1 = first_loc["lat"], first_loc["lng"]
    lat2, lng2 = second_loc["lat"], second_loc["lng"]
    return (
        (lat1 - lat2) ** 2 + (lng1 - lng2) ** 2
    ) ** 0.5 * 111000  # Approximate meter distance


class LocationDeduplicationHandler(BaseHandler):
    def do_handle(self, input_data: str) -> str:
        json_data = json.loads(input_data)

        location_mapping = {}

        for comment in json_data["comments"]:
            for location in comment["locations"]:
                if location["location_name"] not in location_mapping:
                    location_mapping["location_name"] = location["location_name"]
                elif (
                    distance(location, location_mapping[location["location_name"]])
                    <= THRESHOLD
                ):
                    location["lat"] = location_mapping["location_name"]["lat"]
                    location["lng"] = location_mapping["location_name"]["lng"]

        return json.dumps(json_data, indent=4)
