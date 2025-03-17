import json
from src.handlers.reddit.post.add_countries_handler import (
    AddCountriesHandler,
    extract_subreddit,
)


def test_extract_subreddit():
    assert (
        extract_subreddit("https://www.reddit.com/r/japantravel/comments/12345/")
        == "japantravel"
    )
    assert (
        extract_subreddit("https://www.reddit.com/r/travelkorea/comments/12345/")
        == "travelkorea"
    )
    assert (
        extract_subreddit("https://www.reddit.com/r/random/comments/12345/") == "random"
    )
    assert extract_subreddit("https://www.reddit.com/r/") == ""


def test_do_handle():
    input_data = """ 
    [
        {"id": "1", "url": "https://www.reddit.com/r/japantravel/comments/12345/"},
        {"id": "2", "url": "https://www.reddit.com/r/travelkorea/comments/12345/"},
        {"id": "3", "url": "https://www.reddit.com/r/other/comments/12345/"}
    ]
    """

    expected_output = [
        {
            "id": "1",
            "url": "https://www.reddit.com/r/japantravel/comments/12345/",
            "country": "japan",
        },
        {
            "id": "2",
            "url": "https://www.reddit.com/r/travelkorea/comments/12345/",
            "country": "korea",
        },
        {
            "id": "3",
            "url": "https://www.reddit.com/r/other/comments/12345/",
            "country": "unknown",
        },
    ]

    handler = AddCountriesHandler()
    result = handler.do_handle(input_data)
    output_data = json.loads(result)

    assert output_data == expected_output
