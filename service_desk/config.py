import os
from pydantic import BaseModel, Field, HttpUrl, SecretStr


class Settings(BaseModel):
    rag_url: HttpUrl = 'http://127.0.0.1:9991'
    rag_api_key: SecretStr = SecretStr('')
    rag_timeout: float = Field(default=25, gt=0, le=25)

    @classmethod
    def from_env(cls):
        return cls(rag_url=os.getenv('SERVICE_DESK_RAG_URL', 'http://127.0.0.1:9991'),
                   rag_api_key=os.getenv('SERVICE_DESK_RAG_API_KEY', ''),
                   rag_timeout=os.getenv('SERVICE_DESK_RAG_TIMEOUT', '25'))
