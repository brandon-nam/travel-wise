import os
from typing import Any
import openai
from dotenv import load_dotenv
from ai_provider.base_ai_provider import BaseAIProvider

DEFAULT_OPENAI_PARAMS = {"max_tokens": 1000, "temperature": 0.5}


class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def prompt(self, query: str, params: dict[str, Any] = None) -> str:
        if params is None:
            params = DEFAULT_OPENAI_PARAMS

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
            **params
        )

        classification_result = response.choices[0].message.content.strip()
        return classification_result
