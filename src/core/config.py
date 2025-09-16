from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    GROK_API_KEY: str
    GROK_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    GROK_MODEL: str = "llama-3.3-70b-versatile"

    GEMINI_API_KEY: str
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    GEMINI_MODEL: str = "gemini-2.0-flash"

    HUGGING_FACE_API_KEY: str
    HUGGING_FACE_API_URL: str = "https://api-inference.huggingface.co/models/"
    HUGGING_FACE_PROVIDER: str = "Cerebras"
    HUGGING_FACE_MODEL: str = "openai/gpt-oss-120b"

    ONNX_API_URL: str = "http://127.0.0.1:3000/api/onnx/gpt2"

    class Config:
        env_file=".env"

settings = Settings()
