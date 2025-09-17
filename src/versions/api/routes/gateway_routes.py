import traceback

from fastapi import APIRouter, Depends, HTTPException

from ..services.controllers.latency_controller import GatewayLatencyController
from ..services.controllers.history_controller import GatewayHistoryController
from ..services.controllers.race_controller import GatewayRaceController
from ....core.dependencies import (
    get_gateway_history_controller, get_gateway_latency_controller, get_gateway_race_controller
)
from ..services.schemas.gateway_schemas import (
    GatewayRequest, GatewayResponse
)

router = APIRouter()

@router.post("/latency", response_model=GatewayResponse)
async def process_gateway_latency(request: GatewayRequest, gateway_latency_controller: GatewayLatencyController = Depends(get_gateway_latency_controller)):
    try:
        response = await gateway_latency_controller.gateway_latency(request.query)

        return response
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error occurred while fetching data")

@router.post("/race", response_model=GatewayResponse)
async def process_gateway_race(request: GatewayRequest, gateway_race_controller: GatewayRaceController = Depends(get_gateway_race_controller)) :
    try:
        response = await gateway_race_controller.gateway_race(request.query)

        return response
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error occurred while fetching data")
    
@router.post("/history")
async def process_gateway_history(request: GatewayRequest, gateway_history_controller: GatewayHistoryController = Depends(get_gateway_history_controller)):
    try:
        response = await gateway_history_controller.gateway_history(request.query)

        return response
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error occurred while fetching data")

