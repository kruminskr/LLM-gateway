from dotenv import load_dotenv
import httpx
import asyncio
import time
import os

load_dotenv()

# if moved to confing could look cleaner
GROK_MODEL = os.environ.get("GROK_MODEL")
GROK_API_KEY = os.environ.get("GROK_API_KEY")
GROK_API_URL = os.environ.get("GROK_API_URL")

HUGGIN_FACE_MODEL = os.environ.get("HUGGIN_FACE_MODEL")
HUGGIN_FACE_PROVIDER = os.environ.get("HUGGIN_FACE_PROVIDER")
HUGGIN_FACE_API_KEY = os.environ.get("HUGGIN_FACE_API_KEY")
HUGGIN_FACE_API_URL = os.environ.get("HUGGIN_FACE_API_URL")

GEMINI_MODEL = os.environ.get("GEMINI_MODEL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = os.environ.get("GEMINI_API_URL")

# one function that makes the requests and a config file where i configure each ai api
# each AI can be configured with differant models

class AIService:
    def __init__(self):
        self.services = {
            "grok": self.get_groq_response,
            "hf": self.get_data_hugging_face,
            "gemini": self.get_data_gemini,
        }

    async def gateway_latency(self, content: str):
        async with httpx.AsyncClient() as client:
            tasks = [self.measure_latency(client, name, action) for name, action in self.services.items()]

            latencies = await asyncio.gather(*tasks)

            fastest = min(latencies, key=lambda x: x["latency"])

            aiResponse = await fastest["action"](client, content)

            result = {
                "service": fastest["name"],
                "content": aiResponse
            }

            return result

    async def measure_latency(self, client, name, action):
        start_time = time.perf_counter()

        await action(client, "ping") # simple request to measure latency

        end_time = time.perf_counter()

        latency = end_time - start_time

        response = {
            "name": name,
            "latency": latency,
            "action": action
        }

        return response


    async def get_groq_response(self, client, content) -> dict:
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        body = {
            "model": GROK_MODEL,
            "messages": [{"role": "user", "content": content}]
        }
        
        response = await client.post(GROK_API_URL, headers=headers, json=body)
        
        response.raise_for_status()

        return response.json()

    async def get_data_hugging_face(self, client, content) -> dict:
        headers = {
            "Authorization": f"Bearer {HUGGIN_FACE_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": HUGGIN_FACE_MODEL,
            "provider": HUGGIN_FACE_PROVIDER,
            "messages": [{ "role": "user", "content": content }]
        }

        response = await client.post(HUGGIN_FACE_API_URL, headers=headers, json=body)

        response.raise_for_status()

        return response.json()
    
    async def get_data_gemini(self, client, content) -> dict:
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": GEMINI_MODEL,
            "stream": False,
            "messages": [{ "role": "user", "content": content }]
        }

        response = await client.post(GEMINI_API_URL, headers=headers, json=body)

        response.raise_for_status()

        return response.json()


