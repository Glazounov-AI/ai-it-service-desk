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

    async def query(self, query: str, sources: list[str] | None = None) -> RagResponse:
        key = self.settings.rag_api_key.get_secret_value()
        headers = {'X-API-Key': key} if key else {}
        try:
            async with asyncio.timeout(self.settings.rag_timeout):
                response = await self.client.post(
                    str(self.settings.rag_url).rstrip('/') + '/query',
                    json={'query': query, 'mode': 'it_service_desk'} | ({'sources': sources} if sources is not None else {}), headers=headers)
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
            if result.strategy != ('targeted' if sources is not None else 'semantic') or result.query != query:
                raise ValueError('Unexpected response')
            if sources is not None and any(x.get('source') not in sources for x in result.retrieved_sources):
                raise ValueError('Unexpected response')
            return result
        except (ValueError, ValidationError):
            raise RagError(502, 'Некорректный ответ RAG') from None

    async def generate_classification(self, payload):
        key = self.settings.generation_key.get_secret_value()
        headers = {'X-Generation-Key': key}
        if self.settings.rag_api_key.get_secret_value():
            headers['X-API-Key'] = self.settings.rag_api_key.get_secret_value()
        try:
            async with asyncio.timeout(self.settings.generation_timeout):
                response = await self.client.post(
                    str(self.settings.rag_url).rstrip('/') + '/generate',
                    json={'profile': 'it_service_desk_classifier', 'input': payload}, headers=headers)
        except (TimeoutError, httpx.TimeoutException):
            raise RagError(504, 'generation_timeout') from None
        except httpx.RequestError:
            raise RagError(503, 'generation_connection_error') from None
        if response.status_code != 200:
            raise RagError(response.status_code, 'generation_http_error')
        try:
            data = response.json()
            if data['profile'] != 'it_service_desk_classifier' or not isinstance(data['result'], dict):
                raise ValueError()
            usage = data.get('usage', {})
            if not isinstance(usage, dict):
                usage = {}
            return data['result'], {k: v for k, v in usage.items()
                if k in ('input_tokens', 'output_tokens', 'embedding_tokens') and type(v) is int and v >= 0}
        except (ValueError, KeyError, TypeError):
            raise RagError(502, 'invalid_generation_response') from None
