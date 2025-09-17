import httpx
import asyncio

from .....core.ai_api_config import LLM_CONFIG
from ..models.api_model import llm_api_request

class GatewayRaceController:
    async def gateway_race(self, content: str):
        async with httpx.AsyncClient() as client:
            tasks = [
                asyncio.create_task(llm_api_request(client, provider, content))
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