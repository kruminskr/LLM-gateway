import httpx

from .....core.ai_api_config import LLM_CONFIG   
from .....utiles.redis import redis_client
from ..models.api_model import llm_api_request

class GatewayHistoryController:
    async def get_fastest_provider(self):
        fastest_provider = None
        lowest_latency = None

        for provider in LLM_CONFIG.keys():
            data = await redis_client.hgetall(provider)

            if not data:
                continue

            latency = float(data.get("avg_latency"))

            if lowest_latency is None or latency < lowest_latency:
                lowest_latency = latency
                fastest_provider = provider
        
        return fastest_provider

    async def gateway_history(self, content: str):
        fastest_provider = await self.get_fastest_provider()

        if fastest_provider is None: 
            result = await self.gateway_latency(content) # šis
            return result
        
        async with httpx.AsyncClient() as client:
            provider, llm_response = await llm_api_request(client, fastest_provider, content)

            result = {
                "service": provider,
                "content": llm_response
            }

            return result