import asyncio
import httpx
import pytest
from service_desk.rag_client import RagClient, RagError
from service_desk.config import Settings
from service_desk.classification.fallback import unavailable_domain
from service_desk.classification.models import Classification

def test_budget_and_http_error(caplog):
    async def run():
        def handler(request):
            assert int(request.headers['X-Request-Budget-Ms']) == 14250
            return httpx.Response(504)
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            rag = RagClient(client, Settings(generation_timeout=15))
            with pytest.raises(RagError) as exc:
                await rag.generate_classification({})
            assert exc.value.status == 504
            assert str(exc.value) == 'generation_http_error'
    with caplog.at_level('INFO', logger='uvicorn.error'):
        asyncio.run(run())
    assert 'outcome=http_504' in caplog.text

def test_neutral_only_unknown_domain():
    c = Classification(domain='uncertain', confidence=0.4, generation_reason='generation_timeout')
    assert unavailable_domain(c)
    assert not unavailable_domain(c.model_copy(update={'domain':'it_support'}))
    assert not unavailable_domain(c.model_copy(update={'generation_reason':'generation_disabled'}))
