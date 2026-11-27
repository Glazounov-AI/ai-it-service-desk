from .observability import remaining, request_id, stage
import asyncio
import httpx
from pydantic import ValidationError
from .config import Settings
from .models import RagResponse


class RagError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        super().__init__(message)


class UpstreamStatus(Exception):
    def __init__(self, status):
        self.status = status
        super().__init__(f"HTTP {status}")


class RagClient:
    def __init__(self, client: httpx.AsyncClient, settings: Settings):
        self.client = client
        self.settings = settings

    async def _post(self, path, payload, headers, cap):
        with stage(path):
            timeout = remaining(cap)
            if timeout <= 0.75:
                raise TimeoutError("Insufficient upstream budget")
            headers = dict(headers)
            if request_id.get():
                headers['X-Request-ID'] = request_id.get()
            headers['X-Request-Budget-Ms'] = str(max(1, int((timeout-0.75)*1000)))
            async with asyncio.timeout(timeout):
                response = await self.client.post(str(self.settings.rag_url).rstrip('/') + path, json=payload, headers=headers)
                if response.status_code != 200:
                    raise UpstreamStatus(response.status_code)
                return response

    async def query(self, query: str, sources: list[str] | None = None) -> RagResponse:
        key = self.settings.rag_api_key.get_secret_value()
        headers = {'X-API-Key': key} if key else {}
        try:
            response = await self._post('/query', {'query': query, 'mode': 'it_service_desk'} | ({'sources': sources} if sources is not None else {}), headers=headers, cap=self.settings.rag_timeout)
        except UpstreamStatus as exc:
            raise RagError(exc.status if exc.status in (429, 503, 504) else 502, "Ошибка взаимодействия с RAG") from None
        except (TimeoutError, httpx.TimeoutException):
            raise RagError(504, 'Превышено время ожидания RAG') from None
        except httpx.RequestError:
            raise RagError(503, 'RAG недоступен') from None
        if response.status_code == 429:
            raise RagError(429, 'Лимит запросов RAG. Повторите позже.')
        if response.status_code == 503:
            raise RagError(503, 'RAG недоступен')
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

    async def retrieve(self, query: str, sources: list[str]) -> RagResponse:
        key = self.settings.rag_api_key.get_secret_value()
        try:
            response = await self._post('/retrieve', {'query': query, 'mode': 'it_service_desk', 'sources': sources}, {'X-API-Key': key}, self.settings.rag_timeout)
            data = response.json()
            chunks = data['chunks']
            usage = data['usage']
            if data['strategy'] != 'targeted' or not isinstance(chunks, list) or not isinstance(usage, dict):
                raise ValueError()
            if any(usage.get(k) != 0 for k in ('input_tokens', 'output_tokens')):
                raise ValueError()
            if any(not isinstance(c, dict) or c.get('source') not in sources or not isinstance(c.get('text'), str) or not c['text'] for c in chunks):
                raise ValueError()
            return RagResponse(query=query, answer='Поиск завершён.', from_cache=False, model='retrieval-only', strategy='targeted', retrieved_sources=[{'source': c['source'], 'distance': c.get('distance')} for c in chunks], usage={k: usage[k] for k in ('input_tokens','output_tokens','embedding_tokens') if k in usage})
        except UpstreamStatus as exc:
            raise RagError(exc.status if exc.status in (429,503,504) else 502, 'Ошибка поиска RAG') from None
        except (TimeoutError, httpx.TimeoutException):
            raise RagError(504, 'Превышено время ожидания RAG') from None
        except httpx.RequestError:
            raise RagError(503, 'RAG недоступен') from None
        except (ValueError, KeyError, TypeError):
            raise RagError(502, 'Некорректный ответ поиска RAG') from None

    async def generate_classification(self, payload):
        key = self.settings.generation_key.get_secret_value()
        headers = {'X-Generation-Key': key}
        if self.settings.rag_api_key.get_secret_value():
            headers['X-API-Key'] = self.settings.rag_api_key.get_secret_value()
        try:
            response = await self._post('/generate', {'profile': 'it_service_desk_classifier', 'input': payload}, headers=headers, cap=self.settings.generation_timeout)
        except UpstreamStatus as exc:
            raise RagError(exc.status, 'generation_http_error') from None
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
