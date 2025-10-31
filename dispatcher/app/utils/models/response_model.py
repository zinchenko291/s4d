from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Sender(Enum):
    MCPAgent = "MCP-Agent"
    SearchAgent = "Search-Agent"
    NumAgent = "Num-Agent"
    Summary = "Summary"
    GeneralSummary = "General-Summary"



class ResponseModel(BaseModel):
    id: str
    status: bool
    sender: Sender
    payload: Optional[str]

