import asyncio
import httpx
from pydantic import ValidationError
from .config import Settings
from .models import RagResponse


class RagError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        super().__init__(message)


class RagClient:
    def __init__(self, client: httpx.AsyncClient, settings: Settings):
        self.client = client
        self.settings = settings

    async def query(self, query: str) -> RagResponse:
        key = self.settings.rag_api_key.get_secret_value()
        headers = {'X-API-Key': key} if key else {}
        try:
            async with asyncio.timeout(self.settings.rag_timeout):
                response = await self.client.post(
                    str(self.settings.rag_url).rstrip('/') + '/query',
                    json={'query': query, 'mode': 'it_service_desk'}, headers=headers)
        except (TimeoutError, httpx.TimeoutException):
            raise RagError(504, 'Превышено время ожидания RAG') from None
        except httpx.RequestError:
            raise RagError(503, 'RAG недоступен') from None
        if response.status_code == 429:
            raise RagError(429, 'Лимит запросов RAG. Повторите позже.')
        if response.status_code == 504:
            raise RagError(504, 'Превышено время ожидания RAG')
        if response.status_code != 200:
            raise RagError(502, 'Ошибка взаимодействия с RAG')
        try:
            result = RagResponse.model_validate(response.json())
            if result.strategy != 'semantic' or result.query != query:
                raise ValueError('Unexpected response')
            return result
        except (ValueError, ValidationError):
            raise RagError(502, 'Некорректный ответ RAG') from None
