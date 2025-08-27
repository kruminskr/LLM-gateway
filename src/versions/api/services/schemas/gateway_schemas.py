from pydantic import BaseModel

class GatewayLatencyRequest(BaseModel):
    query: str

class GatewayLatencyResponse(BaseModel):
    message: str

class GatewayRaceRequest(BaseModel):
    query: str

class GatewayRaceResponse(BaseModel):
    message: str
