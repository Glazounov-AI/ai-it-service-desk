import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

@pytest.mark.parametrize('mode', ['retrieve','local'])
def test_diagnostic(tmp_path, mode):
    calls=[]
    def handler(req):
        calls.append(req.url.path)
        assert req.url.path == '/retrieve'
        assert req.headers['X-API-Key']=='test-key'
        assert json.loads(req.content)['sources']==['KB-011.md']
        return httpx.Response(200,json={'strategy':'targeted','chunks':[{'source':'KB-011.md','text':'article'}], 'usage':{'input_tokens':0,'output_tokens':0,'embedding_tokens':24}})
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True,diagnostic_lookup=mode,rag_api_key='test-key'),httpx.MockTransport(handler))) as c:
        sid=c.post('/sessions',json={'user_id':'test'}).json()['id']
        r=c.post(f'/sessions/{sid}/messages',json={'query':'VPN подключён, но корпоративные ресурсы недоступны.'})
        assert r.status_code==200
        assert 'повторно подключить VPN' in r.json()['answer']
        assert calls==(['/retrieve'] if mode=='retrieve' else [])
        assert c.get(f'/sessions/{sid}').json()['status']=='awaiting_result'

def test_targeted_consult(tmp_path):
    def handler(req):
        body=json.loads(req.content)
        if req.url.path=='/generate':
            return httpx.Response(200,json={'profile':body['profile'],'result':dict(domain='it_support',category='EMAIL',subcategory='OUTLOOK_START',intent='report_issue',confidence=.95,needs_clarification=False)})
        assert req.url.path=='/query'
        assert body['sources']==['KB-007.md']
        return httpx.Response(200,json=dict(query=body['query'],answer='test',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':'KB-007.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),targeted_consultation=True,generation_enabled=True,generation_key='test'),httpx.MockTransport(handler))) as c:
        r=c.post('/consult',json={'query':'Почтовый клиент зависает на заставке при открытии.'})
        assert r.status_code==200
        assert r.json()['strategy']=='targeted'

def test_neutral_metadata(tmp_path):
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),generation_enabled=True,generation_key='test'),httpx.MockTransport(lambda r:httpx.Response(503)))) as c:
        r=c.post('/consult',json={'query':'Как приготовить борщ?'}).json()
        assert r['answer']==r['classification']['clarification_question']
