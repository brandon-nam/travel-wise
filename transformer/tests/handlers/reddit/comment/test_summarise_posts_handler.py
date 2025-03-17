from handlers.reddit.comment.summarise_posts_handler import (
    SummarisePostsHandler,
)

import unittest
from unittest.mock import patch, MagicMock
import json
from src.handlers.base_ai_handler import BaseAIHandler


class TestSummarisePostsHandler(unittest.TestCase):
    def setUp(self):
        self.mock_ai_provider = MagicMock()
        self.handler = SummarisePostsHandler(ai_provider=self.mock_ai_provider)

    def test_do_handle_basic_functionality(self):
        with patch.object(
            BaseAIHandler, "query_and_load_json"
        ) as mock_query_and_load_json:
            input_data = json.dumps(
                [
                    {"id": "comment1", "text": "Paris is beautiful this time of year!"},
                    {
                        "id": "comment2",
                        "text": "What's the best way to get from the airport to downtown Rome?",
                    },
                ]
            )

            # Setup mock return value
            mock_query_and_load_json.return_value = {
                "comment1": "Paris is known for its beauty, particularly in spring and fall.",
                "comment2": "There are several options to get from the airport to downtown Rome including train, bus, and taxi.",
            }

            # Call the method being tested
            result = self.handler.do_handle(input_data)

            # Parse the result
            result_data = json.loads(result)

            # Assertions
            self.assertEqual(len(result_data), 2)
            self.assertEqual(result_data[0]["id"], "comment1")
            self.assertEqual(
                result_data[0]["summary"],
                "Paris is known for its beauty, particularly in spring and fall.",
            )
            self.assertEqual(result_data[1]["id"], "comment2")
            self.assertEqual(
                result_data[1]["summary"],
                "There are several options to get from the airport to downtown Rome including train, bus, and taxi.",
            )

            # Verify the mock was called with the expected prompt
            expected_prompt_fragment = "Summarize this for the purpose of providing useful travel tips and suggestions."
            mock_query_and_load_json.assert_called_once()
            actual_prompt = mock_query_and_load_json.call_args[0][0]
            self.assertIn(expected_prompt_fragment, actual_prompt)
            self.assertIn(input_data, actual_prompt)
