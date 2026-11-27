import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

@pytest.fixture
def client(tmp_path):
    def upstream(request):
        body = json.loads(request.content)
        return httpx.Response(200,json=dict(query=body['query'],answer='unused',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':body['sources'][0]}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        yield c

def start(c):
    return '/sessions/'+c.post('/sessions',json={'user_id':'final'}).json()['id']

def send(c,url,q):
    r=c.post(url+'/messages',json={'query':q}); assert r.status_code==200,r.text
    return r.json()

@pytest.mark.parametrize('replies,expected',[(['Да','Да'],'resolved'),(['Да','Нет'],'ticket_draft_ready'),(['Нет'],'ticket_draft_ready'),(['Да','Не помогло'],'ticket_draft_ready'),(['Да','Не знаю','Не знаю'],'ticket_draft_ready')])
def test_mfa(client,replies,expected):
    url=start(client); send(client,url,'Сменил телефон')
    for q in replies: send(client,url,q)
    assert client.get(url).json()['status']==expected
    actions=client.get(url+'/diagnostic-case').json()['actions']
    assert actions[0]['status']=='completed'
    if len(actions)==2: assert actions[1]['action_id']=='KB-005:2'
    if expected=='resolved': assert actions[1]['result']=='resolved'

@pytest.mark.parametrize('query',['Outlook не запускается','Не работает Wi-Fi'])
def test_last_completed(client,query):
    url=start(client); send(client,url,query)
    for _ in range(10):
        if client.get(url).json()['status']=='ticket_draft_ready': break
        actions=client.get(url+'/diagnostic-case').json()['actions']
        pending=[a for a in actions if a['status']=='suggested']; assert len(pending)==1
        send(client,url,'Да' if pending[0]['action_type']=='check' else 'Выполнил')
    else: pytest.fail('No terminal state')
    assert client.get(url+'/ticket-draft').json()['troubleshooting_completed']

@pytest.mark.parametrize('reply,complete',[('Ресурсы: intranet.example',True),('Не отображается',False),('Не помогло',False)])
def test_resource_evidence(client,reply,complete):
    url=start(client); send(client,url,'VPN подключён, но корпоративные ресурсы недоступны')
    for q in ['Не помогло','Да','Нет',reply]: send(client,url,q)
    d=client.get(url+'/ticket-draft').json()
    assert d['is_complete']==complete
    assert d['troubleshooting_completed']
    assert d['confirmed_facts'][-1]['text']==reply
