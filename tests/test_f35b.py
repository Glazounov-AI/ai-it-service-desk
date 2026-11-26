import httpx
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings


def test_managed_vpn(tmp_path):
    import json
    calls = []
    def upstream(request):
        body = json.loads(request.content)
        calls.append(body)
        return httpx.Response(200,json=dict(query=body['query'],answer='Непроверенный ответ',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':'KB-011.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        sid = c.post('/sessions',json={'user_id':'test'}).json()['id']
        url = f'/sessions/{sid}'
        def send(q):
            r=c.post(url+'/messages',json={'query':q}); assert r.status_code==200,r.text; return r.json()
        send('Не работает VPN.')
        assert not calls
        send('VPN подключён, но корпоративные ресурсы недоступны.')
        assert calls[0]['sources']==['KB-011.md']
        r=send('Переподключился, но ничего не изменилось.')
        case=c.get(url+'/diagnostic-case').json()
        assert case['subcategory']=='RESOURCE_ACCESS'
        assert case['actions'][0]['status']=='completed'
        assert case['actions'][0]['result']=='not_resolved'
        assert 'кабел' not in r['answer']
        assert len(calls)==1
        send('Всё заработало.')
        assert c.get(url).json()['status']=='resolved'
        assert len(c.get(url+'/messages').json())==8


def test_admin(tmp_path):
    def upstream(request):
        raise AssertionError('No upstream call expected')
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        sid=c.post('/sessions',json={'user_id':'test'}).json()['id']
        url=f'/sessions/{sid}'
        r=c.post(url+'/messages',json={'query':'Дайте мне права администратора.'})
        assert r.status_code==200
        assert c.get(url).json()['status']=='escalation_required'
        assert c.get(url+'/diagnostic-case').json()['support_group']=='Identity & Access'
