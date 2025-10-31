from dataclasses import dataclass


@dataclass
class RegisterSearchTaskResponseDto:
    id: str

    def dump(self):
        return {
            "id": self.id,
        }