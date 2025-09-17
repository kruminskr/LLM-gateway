from .....core.ai_api_config import LLM_CONFIG

async def llm_api_request(client, provider, content) -> dict:
    headers = LLM_CONFIG[provider]["headers"]

    body = {
        **LLM_CONFIG[provider]["body"],
        "messages": [{"role": "user", "content": content}]
    }
    
    response = await client.post(LLM_CONFIG[provider]["url"], headers=headers, json=body)

    response.raise_for_status()

    return provider, response.json()