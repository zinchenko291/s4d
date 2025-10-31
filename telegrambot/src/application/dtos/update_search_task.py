from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateSearchTaskDto:
    status: Optional[int]
    short_summary: Optional[str]
    summary: Optional[str]

    def dump(self):
        return {
            "status": self.status,
            "shortSummary": self.short_summary,
            "summary": self.summary,
        }