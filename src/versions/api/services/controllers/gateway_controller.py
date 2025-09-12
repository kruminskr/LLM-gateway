import httpx
import asyncio
import time

from .....core.llm_config import LLM_CONFIG

class AIService:
    # cons:
    # if one service is really slow the other takss wait on this service
    # request to each serivce and another request to the fastest 

    # TO-DO? when first task is completed stop the rest of the tasks, this kind of defeats the purpose
    async def gateway_latency(self, content: str):
        async with httpx.AsyncClient() as client:
            tasks = [
                asyncio.create_task(
                    asyncio.wait_for(self.measure_latency(client, provider), timeout=3.0)
                )
                for provider in LLM_CONFIG.keys()
            ]

            latencies = await asyncio.gather(*tasks, return_exceptions=True)

            filtered_latencies = [
                req for req in latencies if not isinstance(req, Exception)
            ]

            fastest = min(filtered_latencies, key=lambda x: x["latency"])

            provider, llm_response = await self.llm_api_request(client, fastest["name"], content)

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

        print(f"Requesting {provider}")
        print(f"Status code: {response.status_code}")
        
        response.raise_for_status()

        return provider, response.json()

