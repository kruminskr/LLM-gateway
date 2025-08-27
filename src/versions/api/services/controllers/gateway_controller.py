from dotenv import load_dotenv
import httpx
import os

load_dotenv()

GROK_MODEL = os.environ.get("GROK_MODEL")
GROK_API_KEY = os.environ.get("GROK_API_KEY")
GROK_API_URL = os.environ.get("GROK_API_URL")

class AIService:
    async def get_groq_response(self, content: str) -> dict:
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        body = {
            "model": GROK_MODEL,
            "messages": [{"role": "user", "content": content}]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(GROK_API_URL, headers=headers, json=body)
            response.raise_for_status()
            
        return response.json()

    async def get_data_hugging_face():
        return {"message": "Success"}

    async def get_data_onnx():
        return {"message": "Success"}
