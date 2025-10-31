from dataclasses import dataclass


@dataclass
class NewSearchTaskDto:
    id: str
    request: str

    def dump(self):
        return {
            "id": self.id,
            "payload": self.request,
        }