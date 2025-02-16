import json
import os
from typing import Any
import re

import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_suggestion_or_tip(comments: list[dict[str, Any]]) -> str:
    prompt = f"""
    Please classify the following list of comments into one of the following categories:
    - "travel_suggestion" if it mentions a location you can visit.
    - "travel_tip" if it mentions travel hacks, tips, or advice.
    - "other" if it does not mention any of the above.

    Respond by giving a json object with comment_id as key, and classification as value, 
    stripped of any ```json``` or trailing and leading quotes.

    Comments:
    {comments}
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.5,
    )

    # Extract the classification results from the response
    classification_result = response.choices[0].message.content.strip()
    return classification_result

def classify_location_coordinates(comments: list[dict[str, Any]]) -> str:
    prompt = f"""
    For each location mentioned in these comments, identify their respective coordinates.
    
    Respond with a dictionary where the comment_id is the key and a list of dictionaries as values, where each dictionary contains:
    `"lat"` (latitude, float)
    `"lng"` (longitude, float)
    .
    Make sure it is stripped of any ```json``` or trailing and leading quotes. 
    Do not include any location names anywhere. If there are multiple locations, provide coordinates for all of them. 
    If there are no identifiable locations mentioned, return an empty list instead.
    
    {{
      "mbomop8": [
        {{"lat": 35.3192, "lng": 139.5467}}, 
        {{"lat": 35.4449, "lng": 139.6368}}
      ],
      "mbr1lyf": [
        {{"lat": 35.7719, "lng": 140.3929}}, 
        {{"lat": 35.0116, "lng": 135.7681}}
      ]
    }}

    Comments:
    {comments}
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.5,
    )

    # Extract the classification results from the response
    classification_result = response.choices[0].message.content.strip()
    cleaned_response = re.sub(r"```json\s*([\s\S]*?)\s*```", r"\1", classification_result).strip()
    return cleaned_response


def classify_temporal(comments: list[dict[str, Any]]) -> dict[str,str | None]:
    prompt = f"""
    Identify a date range with a start and end date from these comments. 
    If an exact date is mentioned, return that date as both the start and end dates.
    If a specific date range is mentioned, return the respective start date and end date.
    If a season is mentioned, approximate a two-week date range and return the respective start date and end date.
    If no dates are found, return null for both.
    
    Return a dictionary with the following structure where the comment_id is the key and the dictionary is the value, stripped of any ```json``` or trailing and leading quotes:
    {{
        "start_date": "YYYY-MM-DD" | null,
        "end_date": "YYYY-MM-DD" | null
    }}
    
    Do not return any other text.

    Comments:
    {comments}
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.5,
    )

    # Extract the classification results from the response
    classification_result = response.choices[0].message.content.strip()
    cleaned_response = re.sub(r"```json\s*([\s\S]*?)\s*```", r"\1", classification_result).strip()
    parsed_response = json.loads(cleaned_response)
    return parsed_response




def main():
    input_file = "JapanTravel_2025-02-10 22:29.json"
    with open(f"./{input_file}") as f:
        data = json.load(f)

    classification_map = {}
    coordinate_map = {}

    for post in data:
        location_result = classify_location_coordinates(post["comments"])
        classification_map.update(json.loads(location_result))

        suggest_result = classify_suggestion_or_tip(post["comments"])
        coordinate_map.update(json.loads(suggest_result))

    for post in data:
        for comment in post["comments"]:

            location_data = {"locations": classification_map.get(comment["id"], "unknown")}
            suggest_data = {"classification": coordinate_map.get(comment["id"], "unknown")}


            date_data = classify_temporal(comment)
            extract_date = date_data.get(comment["id"], {"start_date": None, "end_date": None})
            comment.update({
                **suggest_data,
                **location_data,
                **extract_date

            })

    with open(f"./transformed_{input_file}", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
