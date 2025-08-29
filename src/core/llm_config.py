from dotenv import load_dotenv
import os

load_dotenv()

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

ONNX_API_URL = os.environ.get("ONNX_API_URL")

LLM_CONFIG = {
    "grok": {
        "url": GROK_API_URL,
        "headers": {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        },
        "body": {
            "model": GROK_MODEL,
        }
    },
    "hugging_face": {
        "url": HUGGIN_FACE_API_URL,
        "headers": {
            "Authorization": f"Bearer {HUGGIN_FACE_API_KEY}",
            "Content-Type": "application/json"
        },
        "body": {
            "model": HUGGIN_FACE_MODEL,
            "provider": HUGGIN_FACE_PROVIDER,
        }
    },
    "gemini": {
        "url": GEMINI_API_URL,
        "headers": {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        },
        "body": {
            "model": GEMINI_MODEL,
            "stream": False,
        }
    },
    "onnx": {
        "url": ONNX_API_URL,
        "headers": {
            # 
        },
        "body": {
            # 
        }
    }
}