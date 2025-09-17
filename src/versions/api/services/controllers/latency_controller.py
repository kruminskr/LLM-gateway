import httpx
import asyncio
import time

from .....core.ai_api_config import LLM_CONFIG   
from ..models.api_model import llm_api_request
from ..models.redis_model import set_redis_cache

class GatewayLatencyController:
    async def gateway_latency(self, content: str):
        async with httpx.AsyncClient() as client:
            tasks = [
                asyncio.create_task(
                    asyncio.wait_for(self.measure_latency(client, provider), timeout=2.0)
                )
                for provider in LLM_CONFIG.keys()
            ]

            latencies = await asyncio.gather(*tasks, return_exceptions=True)

            filtered_latencies = [
                req for req in latencies if not isinstance(req, Exception)
            ]

            fastest = min(filtered_latencies, key=lambda x: x["latency"])

            provider, llm_response = await llm_api_request(client, fastest["name"], content)

            for item in filtered_latencies:
                await set_redis_cache(item["name"], item["latency"])
                
            result = {
                "service": provider,
                "content": llm_response
            }

            return result

    async def measure_latency(self, client, provider):
        start_time = time.perf_counter()

        await llm_api_request(client, provider, "ping") # simple request to measure latency

        end_time = time.perf_counter()

        latency = end_time - start_time

        response = {
            "name": provider,
            "latency": latency,
        }

        return response