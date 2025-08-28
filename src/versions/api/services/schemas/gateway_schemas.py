from pydantic import BaseModel
from typing import Any, List

class GatewayRequest(BaseModel):
    query: str

class GatewayResponse(BaseModel):
    service: str
    content: dict
