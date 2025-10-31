import json
import os

class AiConfig:
    def __init__(self, **kwargs):
        self.TOKEN = kwargs.get('TOKEN', "")
        self.BASE_MODEL = kwargs.get('BASE_MODEL', "")
        self.BASE_URL = kwargs.get("BASE_URL", "AAAAA")
        self.TOKEN_LIMIT = kwargs.get('TOKEN_LIMIT', 1)
        if self.TOKEN_LIMIT > 1000:
            self.TOKEN_LIMIT = 1000
        elif self.TOKEN_LIMIT < 1:
            self.TOKEN_LIMIT = 1
        self.MAX_RETRIES = kwargs.get('MAX_RETRIES', 3)

    def dump(self):
        return self.__dict__


class EndpointConfig:
    def __init__(self, **kwargs):
        self.HOST = kwargs.get('HOST', "")
        self.PORT = kwargs.get('PORT', "")
        self.ALLOWED_HOST = kwargs.get('ALLOWED_HOST', tuple())

    def dump(self):
        return self.__dict__


class Config:
    """ Singleton-класс для загрузки конфигурации из JSON. """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        with open("config.json", "r") as file:
            data = json.load(file)
            self.BASE_URL = os.getenv("BASE_URL")
            self.API_KEY = data.get("API_KEY", "")
            self.BOT_TOKEN = os.getenv("BOT_TOKEN", "")
            self.REDIS_HOST = data.get("REDIS_HOST", "localhost")
            self.REDIS_PORT = data.get("REDIS_PORT", 1000)
            self.REDIS_DB = data.get("REDIS_DB", 0)
            self.RABBIT_USER = os.getenv("RABBIT_USER")
            self.RABBIT_PASS = os.getenv("RABBIT_PASS")
            self.RABBIT_HOST = os.getenv("RABBIT_HOST")
            self.RABBIT_PORT = os.getenv("RABBIT_PORT")
            self.LANGUAGES_FOLDER = data.get("LANGUAGES_FOLDER", "src/infrastructure/localization")
            self.AI = AiConfig(**data.get("AI", dict()))
            self.ENDPOINT = EndpointConfig(**data.get("ENDPOINT", dict()))

        self.save_config()

    def save_config(self):
        with open("config.json", "w") as file:
            file.write(json.dumps({
                "BASE_URL": self.BASE_URL,
                "API_KEY": self.API_KEY,
                "BOT_TOKEN": self.BOT_TOKEN,
                "REDIS_HOST": self.REDIS_HOST,
                "REDIS_PORT": self.REDIS_PORT,
                "REDIS_DB": self.REDIS_DB,
                "RABBIT_USER": self.RABBIT_USER,
                "RABBIT_PASS": self.RABBIT_PASS,
                "RABBIT_HOST": self.RABBIT_HOST,
                "RABBIT_PORT": self.RABBIT_PORT,
                "LANGUAGES_FOLDER": self.LANGUAGES_FOLDER,
                "AI": self.AI.dump(),
                "ENDPOINT": self.ENDPOINT.dump(),
            }, indent=4))
