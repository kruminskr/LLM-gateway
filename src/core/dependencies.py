from ..versions.api.services.controllers.gateway_controller import AIService

from ..versions.api.services.controllers.history_controller import GatewayHistoryController
from ..versions.api.services.controllers.latency_controller import GatewayLatencyController
from ..versions.api.services.controllers.race_controller import GatewayRaceController

def get_gateway_history_controller() -> GatewayHistoryController:
    return GatewayHistoryController()

def get_gateway_latency_controller() -> GatewayLatencyController:
    return GatewayLatencyController()

def get_gateway_race_controller() -> GatewayRaceController:
    return GatewayRaceController()