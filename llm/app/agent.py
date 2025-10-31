from openai import OpenAI
from typing import Optional

from .prompt import Prompt


class Agent(OpenAI):
    def __init__(
            self, model: str, prompt: Prompt,
            api_key: str, base_url: str,
            project: str,
            temperature: float = 0.3,
            max_output_tokens: int = 1500):

        self.model: str = model
        self.prompt: Prompt = prompt
        self.temperature: float = temperature
        self.max_output_tokens: int = max_output_tokens

        super().__init__(
            api_key=api_key,
            base_url=base_url,
            project=project
        )


    def Ask(self, message: str, tools: list = []) -> Optional[str]:
        response = self.responses.create(
            model=self.model,
            instructions=self.prompt.GetPrompt(),
            input=message,
            max_output_tokens=self.max_output_tokens,
            temperature=self.temperature,
            tools=tools
        )

        if response.output_text == "0":
            return None

        return response.output_text

