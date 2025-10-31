from pydantic import BaseModel
from typing import Optional


class ResponseModel(BaseModel):
    id: str
    status: bool
    sender: str
    payload: Optional[str] = None

