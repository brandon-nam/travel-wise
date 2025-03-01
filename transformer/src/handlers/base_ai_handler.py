import json
from abc import ABC

from src.ai_provider.base_ai_provider import BaseAIProvider
from src.handlers.base_handler import BaseHandler


class BaseAIHandler(BaseHandler, ABC):
    def __init__(self, ai_provider: BaseAIProvider):
        self.ai_provider = ai_provider

    def query_and_load_json(self, prompt: str) -> dict:
        """
        Given a prompt, return a dictionary object. Make sure the prompt
        tells the model to return a JSON object.
        """
        query_result = self.ai_provider.prompt(prompt)
        return json.loads(query_result)
