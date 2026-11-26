import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings
from service_desk.classification.taxonomy import ROOT


def test_prompt_contract():
    prompt = (ROOT / 'generation/prompt.md').read_text(encoding='utf-8')
    for phrase in ('NOT relevance', 'out_of_scope', 'report_failure', 'VPN/RESOURCE_ACCESS', 'latest user facts', 'not evidence'):
        assert phrase in prompt


@pytest.mark.parametrize('domain,confidence,clarify,expected', [
    ('out_of_scope', .95, False, 'local-out-of-scope'),
    ('out_of_scope', .1, False, 'local-clarification'),
    ('uncertain', .95, True, 'local-clarification'),
])
def test_domain_contract(tmp_path, domain, confidence, clarify, expected):
    def handler(req):
        assert req.url.path == '/generate'
        body = json.loads(req.content)
        return httpx.Response(200, json={'profile':body['profile'], 'result':dict(domain=domain, category=None, subcategory=None, intent='unknown', confidence=confidence, needs_clarification=clarify)})
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'), generation_enabled=True, generation_key='test'), httpx.MockTransport(handler))) as c:
        result = c.post('/consult', json={'query':'Как приготовить борщ?'}).json()
        assert result['model'] == expected


def test_followup_intent_contract(tmp_path):
    def handler(req):
        body = json.loads(req.content)
        if req.url.path == '/query':
            return httpx.Response(200, json=dict(query=body['query'], answer='test', model='test', from_cache=False))
        history = body['input']['history']
        if not history:
            result = dict(domain='uncertain', category=None, subcategory=None, intent='unknown', confidence=.95, needs_clarification=True)
        else:
            assert any('VPN' in m['content'] for m in history if m['role']=='user')
            result = dict(domain='it_support', category='VPN', subcategory='RESOURCE_ACCESS', intent='report_failure', confidence=.9, needs_clarification=False)
        return httpx.Response(200, json=dict(profile=body['profile'], result=result))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'), generation_enabled=True, generation_key='test'), httpx.MockTransport(handler))) as c:
        sid = c.post('/sessions', json={'user_id':'a'}).json()['id']
        c.post(f'/sessions/{sid}/messages', json={'query':'VPN подключён, корпоративные ресурсы недоступны.'})
        r = c.post(f'/sessions/{sid}/messages', json={'query':'Переподключился, но ничего не изменилось.'}).json()
        assert r['classification']['subcategory']=='RESOURCE_ACCESS'
        assert r['classification']['intent']=='report_failure'
