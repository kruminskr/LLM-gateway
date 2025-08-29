from fastapi import APIRouter, Depends, HTTPException

from ....core.dependencies import get_ai_service
from ..services.controllers.gateway_controller import AIService
from ..services.schemas.gateway_schemas import (
    GatewayRequest,
    GatewayResponse,
)

router = APIRouter()

# add error handler

@router.post("/latency", response_model=GatewayResponse)
async def process_gateway_latency(request: GatewayRequest, ai_service: AIService = Depends(get_ai_service)):
    try:
        response = await ai_service.gateway_latency(request.query)

        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error occurred while fetching data")

@router.post("/race", response_model=GatewayResponse)
async def process_gateway_race(request: GatewayRequest, ai_service: AIService = Depends(get_ai_service)):
    try:
        response = await ai_service.gateway_race(request.query)

        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error occurred while fetching data")
    


