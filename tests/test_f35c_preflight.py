import httpx
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings


def test_no_context_and_vague_vpn_skip_generation(tmp_path):
    def upstream(request):
        raise AssertionError('Unexpected upstream request')
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True,generation_enabled=True,generation_key='test'),httpx.MockTransport(upstream))) as c:
        for query in ['Переподключился, но ничего не изменилось.', 'Всё заработало.', 'Не работает VPN.']:
            sid=c.post('/sessions',json={'user_id':'test'}).json()['id']
            url=f'/sessions/{sid}'
            r=c.post(url+'/messages',json={'query':query})
            assert r.status_code==200,r.text
            assert r.json()['classification']['needs_clarification']
            assert r.json()['classification']['subcategory'] is None
            assert c.get(url).json()['status']=='clarifying'


def test_active_followup_skips_generation(tmp_path):
    import json
    calls=[]
    def upstream(request):
        assert request.url.path == '/query'
        body=json.loads(request.content)
        calls.append(body)
        return httpx.Response(200,json=dict(query=body['query'],answer='test',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':'KB-011.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True,generation_enabled=True,generation_key='test'),httpx.MockTransport(upstream))) as c:
        sid=c.post('/sessions',json={'user_id':'test'}).json()['id']
        url=f'/sessions/{sid}'
        def send(q):
            r=c.post(url+'/messages',json={'query':q}); assert r.status_code==200,r.text; return r.json()
        send('Не работает VPN.')
        send('VPN подключён, но корпоративные ресурсы недоступны.')
        assert send('Переподключился, но ничего не изменилось.')['classification']['intent']=='report_failure'
        assert send('Всё заработало.')['classification']['intent']=='confirm_resolution'
        assert c.get(url).json()['status']=='resolved'
        assert len(calls)==1
