from pydantic import BaseModel

class GatewayRequest(BaseModel):
    query: str

class GatewayResponse(BaseModel):
    service: str
    content: dict
