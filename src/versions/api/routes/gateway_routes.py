from fastapi import APIRouter, Depends, HTTPException

from ....core.dependencies import get_ai_service
from ..services.controllers.gateway_controller import AIService
from ..services.schemas.gateway_schemas import (
    GatewayLatencyRequest, 
    GatewayLatencyResponse,
    GatewayRaceRequest,
    GatewayRaceResponse
)

router = APIRouter()

@router.post("/gateway/latency", response_model=GatewayLatencyResponse)
async def gateway_latency(
    request: GatewayLatencyRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    try:
        result = await ai_service.get_groq_response(request.query)

        print(result)

        return {"message": "Success"}
    except Exception as erorr:
        print(erorr)
        raise HTTPException(
            status_code=500, 
            detail="Error occurred while fetching data"
        )

@router.post("/gateway/race")
async def gateway_race():
    return {"message": "Success"}
