from pydantic import BaseModel
from typing import Union, Optional


class ResultPayload(BaseModel):
    shortSummary: str
    summary: str


class Result(BaseModel):
    id: str
    status: bool
    payload: Optional[Union[str, ResultPayload]] = None
