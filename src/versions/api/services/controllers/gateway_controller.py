import httpx
import asyncio
import time

from .....core.llm_config import LLM_CONFIG

class AIService:
    # add exception handling - fallback service
    # if fastest fails, the route to the second fastest
    async def gateway_latency(self, content: str):
        async with httpx.AsyncClient() as client:
            tasks = [self.measure_latency(client, provider) for provider in LLM_CONFIG.keys()]

            # TO-DO? when first task is completed stop the rest of the tasks, this kind of defeats the purpose
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
    
    # add exception handling - fallback service
    # if fastest fails, restart the service again?
    async def gateway_race(self, content: str):
        async with httpx.AsyncClient() as client:
            tasks = [
                asyncio.create_task(self.llm_api_request(client, provider, content))
                for provider in LLM_CONFIG.keys()
            ]            

            async for completed_task in asyncio.as_completed(tasks):
                provider, llm_response = await completed_task

                for task in tasks:
                    if not task.done():
                        task.cancel()

                result = {
                    "service": provider,
                    "content": llm_response
                }

                return result
    
    async def llm_api_request(self, client, provider, content) -> dict:
        headers = LLM_CONFIG[provider]["headers"]

        body = {
            **LLM_CONFIG[provider]["body"],
            "messages": [{"role": "user", "content": content}]
        }
        
        response = await client.post(LLM_CONFIG[provider]["url"], headers=headers, json=body)
        
        response.raise_for_status()

        return provider, response.json()

