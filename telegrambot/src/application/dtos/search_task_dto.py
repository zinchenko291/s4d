from dataclasses import dataclass


@dataclass
class SearchTaskDto:
    telegram_id: int
    message_id: int

    def dump(self):
        return {
            "telegramId": self.telegram_id,
            "messageId": self.message_id,
        }