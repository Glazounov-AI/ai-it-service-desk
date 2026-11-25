import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings


def make_client(handler):
    return TestClient(create_app(Settings(rag_api_key='test-key'), httpx.MockTransport(handler)))


def test_success():
    def handler(request):
        assert request.url.path == '/query'
        assert request.headers['X-API-Key'] == 'test-key'
        assert json.loads(request.content) == {'query': 'VPN', 'mode': 'it_service_desk'}
        return httpx.Response(200, json={'query':'VPN','answer':'Проверьте подключение', 'model':'test','from_cache':False})
    with make_client(handler) as client:
        assert client.get('/health').status_code == 200
        response = client.post('/consult', json={'query':' VPN '})
        assert response.status_code == 200
        assert response.json()['answer'] == 'Проверьте подключение'


@pytest.mark.parametrize('query', ['', '   ', 'x'*2001])
def test_invalid(query):
    with make_client(lambda r: pytest.fail('Unexpected upstream call')) as client:
        assert client.post('/consult', json={'query':query}).status_code == 422


@pytest.mark.parametrize('upstream,expected', [(401,502),(422,502),(429,429),(500,502),(504,504)])
def test_errors(upstream, expected):
    with make_client(lambda r: httpx.Response(upstream, text='secret upstream detail')) as client:
        response = client.post('/consult', json={'query':'VPN'})
        assert response.status_code == expected
        assert 'secret' not in response.text


@pytest.mark.parametrize('error,expected', [(httpx.ConnectError,503),(httpx.ReadTimeout,504)])
def test_transport(error, expected):
    def handler(request):
        raise error('internal detail', request=request)
    with make_client(handler) as client:
        assert client.post('/consult', json={'query':'VPN'}).status_code == expected


def test_bad_response():
    with make_client(lambda r: httpx.Response(200,json={'answer':'x'})) as client:
        assert client.post('/consult', json={'query':'VPN'}).status_code == 502
