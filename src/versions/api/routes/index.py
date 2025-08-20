from fastapi import APIRouter

from ..services.controllers import api_controller as apiController

router = APIRouter()

@router.get("/predict/latancy")
def getData(): return apiController.getDataLatency()

@router.get("/predict/race")
def getData(): return apiController.getDataRace()

