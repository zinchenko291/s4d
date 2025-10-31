from pydantic import BaseModel
from typing import Optional


class Payload(BaseModel):
    num: Optional[str] = None
    mcp_response: Optional[str] = None
    web_search_response: Optional[str] = None
    summary: Optional[str] = None
    general_summary: Optional[str] = None


class Task(BaseModel):
    id: str
    stage: int
    request: str
    payload: Payload
