import os
from typing import Any
import openai
from dotenv import load_dotenv

from src.ai_provider.base_ai_provider import BaseAIProvider

DEFAULT_OPENAI_PARAMS = {"max_tokens": 3000, "temperature": 0.5}


class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.fine_tuned_model_id = None

    def set_fine_tuned_model(self, fine_tuning_job_id: str) -> None:
        # Retrieve the fine-tuned model ID after the fine-tuning job completes
        job_response = self.client.fine_tuning.jobs.retrieve(fine_tuning_job_id)
        self.fine_tuned_model_id = job_response['fine_tuned_model']
        print(f"Fine-tuned model ID: {self.fine_tuned_model_id}")

    def prompt(self, query: str, params: dict[str, Any] = None) -> str:
        if params is None:
            params = DEFAULT_OPENAI_PARAMS

        model_id = self.fine_tuned_model_id if self.fine_tuned_model_id else "gpt-4-turbo"
        response = self.client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
            **params
        )

        classification_result = response.choices[0].message.content.strip()
        return classification_result
