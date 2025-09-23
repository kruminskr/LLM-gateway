from .config import settings

LLM_CONFIG = {
    "grok": {
        "url": settings.GROK_API_URL,
        "headers": {
            "Authorization": f"Bearer {settings.GROK_API_KEY}",
            "Content-Type": "application/json"
        },
        "body": {
            "model": settings.GROK_MODEL,
        }
    },
    
    "hugging_face": {
        "url": settings.HUGGING_FACE_API_URL,
        "headers": {
            "Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}",
            "Content-Type": "application/json"
        },
        "body": {
            "model": settings.HUGGING_FACE_MODEL,
            "provider": settings.HUGGING_FACE_PROVIDER,
        }
    },

    "gemini": {
        "url": settings.GEMINI_API_URL,
        "headers": {
            "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
            "Content-Type": "application/json"
        },
        "body": {
            "model": settings.GEMINI_MODEL,
            "stream": False,
        }
    },

    # "onnx": {
    #     "url": settings.ONNX_API_URL,
    #     "headers": {
    #         # 
    #     },
    #     "body": {
    #         # 
    #     }
    # }
}