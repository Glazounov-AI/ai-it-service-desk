import os
from pydantic import BaseModel, Field, HttpUrl, SecretStr


class Settings(BaseModel):
    db_path: str = Field(default='data/service_desk.db', min_length=1)
    rag_url: HttpUrl = 'http://127.0.0.1:9991'
    rag_api_key: SecretStr = SecretStr('')
    rag_timeout: float = Field(default=25, gt=0, le=25)

    generation_confidence_threshold: float = Field(default=0.8, ge=0, le=1)
    generation_enabled: bool = False
    generation_key: SecretStr = SecretStr('')
    generation_timeout: float = Field(default=10, gt=0, le=15)

    @classmethod
    def from_env(cls):
        return cls(db_path=os.getenv('SERVICE_DESK_DB_PATH', 'data/service_desk.db'),
                   rag_url=os.getenv('SERVICE_DESK_RAG_URL', 'http://127.0.0.1:9991'),
                   rag_api_key=os.getenv('SERVICE_DESK_RAG_API_KEY', ''),
                   rag_timeout=os.getenv('SERVICE_DESK_RAG_TIMEOUT', '25'),
                   generation_confidence_threshold=os.getenv('SERVICE_DESK_GENERATION_CONFIDENCE_THRESHOLD', '0.8'),
                   generation_enabled=os.getenv('SERVICE_DESK_GENERATION_ENABLED', 'false'),
                   generation_key=os.getenv('SERVICE_DESK_GENERATION_KEY', ''),
                   generation_timeout=os.getenv('SERVICE_DESK_GENERATION_TIMEOUT', '10'))
