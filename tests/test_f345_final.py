import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

@pytest.mark.parametrize('variant,reason,status,method', [
 ('valid','llm_classification_accepted',200,'llm'),
 ('low','confidence_below_threshold',200,'fallback'),
 ('403','generation_http_error',403,'fallback'),
 ('429','generation_http_error',429,'fallback'),
 ('timeout','generation_timeout',504,'fallback'),
 ('connection','generation_connection_error',503,'fallback'),
 ('invalid','invalid_generation_response',200,'fallback'),
 ('outside','llm_classification_accepted',200,'llm'),
 ('conflict','domain_conflict',200,'fallback'),
])
def test_diagnostics(tmp_path,variant,reason,status,method):
    calls=[]
    def handler(req):
        calls.append(req.url.path)
        body=json.loads(req.content)
        if req.url.path=='/query':
            return httpx.Response(200,json=dict(query=body['query'],answer='test',model='test',from_cache=False))
        if variant in ('403','429'): return httpx.Response(int(variant))
        if variant=='timeout': raise httpx.ReadTimeout('secret',request=req)
        if variant=='connection': raise httpx.ConnectError('secret',request=req)
        result=dict(domain='it_support',category='EMAIL',subcategory='OUTLOOK_START',intent='report_issue',confidence=.8,needs_clarification=False)
        if variant=='low': result['confidence']=.79
        if variant=='invalid': result['confidence']='bad'
        if variant in ('outside','conflict'): result.update(domain='out_of_scope',category=None,subcategory=None,intent='unknown')
        return httpx.Response(200,json=dict(profile=body['profile'],result=result,usage=dict(input_tokens=365,output_tokens=34,embedding_tokens=0)))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),generation_enabled=True,generation_key='test'),httpx.MockTransport(handler))) as c:
        r=c.post('/consult',json={'query':'Как приготовить борщ?' if variant=='outside' else 'Почтовый клиент зависает на заставке при открытии.'}).json()
        cls=r['classification']
        assert (cls['generation_reason'],cls['generation_http_status'],cls['method'])==(reason,status,method)
        assert cls['generation_usage']==({'input_tokens':365,'output_tokens':34,'embedding_tokens':0} if status==200 else {})
        assert calls==(['/generate','/query'] if variant=='valid' else ['/generate'])
        if variant=='outside': assert r['model']=='local-out-of-scope'

def test_session_context(tmp_path):
    histories=[]
    def handler(req):
        body=json.loads(req.content)
        if req.url.path=='/query': return httpx.Response(200,json=dict(query=body['query'],answer='test',model='test',from_cache=False))
        history=body['input']['history']; histories.append(history)
        result=dict(domain='uncertain',category=None,subcategory=None,intent='unknown',confidence=.9,needs_clarification=True)
        if history and 'VPN' in history[0]['content']:
            result.update(domain='it_support',category='VPN',subcategory='RESOURCE_ACCESS',intent='provide_details',needs_clarification=False)
        return httpx.Response(200,json=dict(profile=body['profile'],result=result))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),generation_enabled=True,generation_key='test'),httpx.MockTransport(handler))) as c:
        a=c.post('/sessions',json={'user_id':'a'}).json()['id']; b=c.post('/sessions',json={'user_id':'b'}).json()['id']
        c.post(f'/sessions/{a}/messages',json={'query':'Не работает VPN.'})
        query='Соединение установлено, но внутренние ресурсы недоступны.'
        x=c.post(f'/sessions/{a}/messages',json={'query':query}).json(); y=c.post(f'/sessions/{b}/messages',json={'query':query}).json()
        assert x['classification']['subcategory']=='RESOURCE_ACCESS'
        assert y['classification']['needs_clarification']
        assert len(histories[1])==2 and histories[2]==[]
