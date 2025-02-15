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
    - "unrelated" if it does not mention any of the above.

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
    Respond by giving a json object string with comment_id as key and a dictionary containing the coordinates as the value, 
    stripped of any ```json``` or trailing and leading quotes. 
    If there are no identifiable locations mentioned, return an empty dictionary instead.
    
    Example format:
    {{
      "Tokyo": [35.6895, 139.6917],
      "Kamakura": [35.3192, 139.5467]
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
    #print(f"🔍 Raw OpenAI response: {repr(classification_result)}")  # Use repr() to show hidden characters
    cleaned_response = re.sub(r"```json\s*([\s\S]*?)\s*```", r"\1", classification_result).strip()
    return cleaned_response


def main():
    input_file = "JapanTravel_2025-02-10 22:29.json"
    with open(f"./{input_file}") as f:
        data = json.load(f)

    classification_map = {}

    for post in data:
        result = classify_location_coordinates(post["comments"])
        classification_map.update(json.loads(result))

    for post in data:
        for comment in post["comments"]:
            comment.update(
                {"classification": classification_map.get(comment["id"], "unknown")}
            )

    with open(f"./transformed_3_{input_file}", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
