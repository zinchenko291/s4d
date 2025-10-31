from pydantic import BaseModel


class RequestModel(BaseModel):
    id: str
    payload: str
