import httpx
import asyncio
import time

from .....core.ai_api_config import LLM_CONFIG
from .....utiles.redis import redis_client

class AIService:
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

            provider, llm_response = await self.llm_api_request(client, fastest["name"], content)

            for item in filtered_latencies:
                await self.set_redis_cache(item["name"], item["latency"])
                
            result = {
                "service": provider,
                "content": llm_response
            }

            return result

    async def measure_latency(self, client, provider):
        start_time = time.perf_counter()

        await self.llm_api_request(client, provider, "ping") # simple request to measure latency

        end_time = time.perf_counter()

        latency = end_time - start_time

        response = {
            "name": provider,
            "latency": latency,
        }

        return response
    
    async def gateway_race(self, content: str):
        async with httpx.AsyncClient() as client:
            tasks = [
                asyncio.create_task(self.llm_api_request(client, provider, content))
                for provider in LLM_CONFIG.keys()
            ]

            while tasks:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                
                for task in done:
                    try:
                        provider, llm_response = await task
                        
                        for pending_task in pending:
                            pending_task.cancel()
                        
                        result = {
                            "service": provider,
                            "content": llm_response
                        }
                        
                        return result
                        
                    except Exception:
                        continue
                
                tasks = list(pending)
    
    async def llm_api_request(self, client, provider, content) -> dict:
        headers = LLM_CONFIG[provider]["headers"]

        body = {
            **LLM_CONFIG[provider]["body"],
            "messages": [{"role": "user", "content": content}]
        }
        
        response = await client.post(LLM_CONFIG[provider]["url"], headers=headers, json=body)

        response.raise_for_status()

        return provider, response.json()
    
    async def set_redis_cache(self, provider, latency):
        previos_data = await redis_client.hgetall(provider)
        
        EMA_ALPHA = 0.3 # Smoothing factor for EMA 

        if previos_data:
            old_avg_latency = float(previos_data.get("avg_latency"))
            avg_latency = EMA_ALPHA * latency + (1-EMA_ALPHA) * old_avg_latency

        if not previos_data:
            avg_latency = latency

        data = {
            "avg_latency": avg_latency,
            "last_latency": latency,
            "last_updated": time.time()
        }

        async with redis_client.pipeline() as pipe:
            await pipe.hset(provider, mapping=data)
            await pipe.expire(provider, 600)
            await pipe.execute()
    
    async def gateway_history(self, content: str):
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

        if fastest_provider is None: 
            result = await self.gateway_latency(content)
            return result
        
        async with httpx.AsyncClient() as client:
            provider, llm_response = await self.llm_api_request(client, fastest_provider, content)

            result = {
                "service": provider,
                "content": llm_response
            }

            return result

        # health check path for latencies

