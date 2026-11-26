import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

@pytest.mark.parametrize('variant', ['valid','invalid_pair','unavailable','low_confidence','conflict'])
def test_hybrid(tmp_path, variant):
    calls=[]
    def handler(r):
        calls.append(r.url.path)
        body=json.loads(r.content)
        if r.url.path=='/generate':
            assert r.headers['X-Generation-Key']=='test'
            assert body['profile']=='it_service_desk_classifier'
            result=dict(domain='it_support',category='VPN',subcategory='CONNECTION',intent='report_issue',confidence=.9,needs_clarification=False)
            if variant=='invalid_pair': result['subcategory']='invented'
            if variant=='low_confidence': result['confidence']=.3
            if variant=='conflict': result.update(category='EMAIL',subcategory='OUTLOOK_START')
            if variant=='unavailable': return httpx.Response(503)
            return httpx.Response(200,json={'profile':body['profile'],'result':result})
        return httpx.Response(200,json={'query':body['query'],'answer':'test','model':'test','from_cache':False})
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),generation_enabled=True,generation_key='test'),httpx.MockTransport(handler))) as c:
        r=c.post('/consult',json={'query':'VPN'}).json()
        assert r['classification']['method']==('llm' if variant=='valid' else 'fallback')
        assert calls==(['/generate','/query'] if variant=='valid' else ['/generate'])
        calls.clear()
        c.post('/consult',json={'query':'Не подключается VPN'})
        assert calls==['/query']
        calls.clear()
        c.post('/consult',json={'query':'Пароль: testSecret123'})
        assert not calls

def test_context():
    from service_desk.context import build_context
    from service_desk.safety import SafetyFilter
    messages=[{'role':'user','content':'a'*1000} for _ in range(8)]+[{'role':'user','content':'Пароль: testSecret123'}]
    result=build_context(messages,SafetyFilter())
    assert sum(len(x['content']) for x in result)<=2400
    assert all(len(x['content'])<=600 for x in result)
    assert 'testSecret123' not in str(result)
