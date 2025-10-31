import yaml

class Prompt:
    _prompt: str

    def __init__(self, file_path: str, prompt_name: str):
        with open(file_path, "r", encoding="utf-8") as file:
            self._prompt = yaml.safe_load(file)[prompt_name]["instruction"]


    def GetPrompt(self, **kwargs) -> str:
        return self._prompt.format(**kwargs)
