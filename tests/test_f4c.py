import csv
import json
from pathlib import Path
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

ROOT = Path(__file__).resolve().parents[1]
with (ROOT/'knowledge-base/it-knowledge-base.csv').open(encoding='utf-8-sig') as f:
    ARTICLES = list(csv.DictReader(f, delimiter=';'))
QUERIES = ['Забыл пароль','Учётная запись заблокирована','Не удаётся войти в корпоративную учётную запись','Не приходит код MFA','Сменил телефон','Authenticator не подтверждает вход','Outlook не запускается','Не отправляются письма','VPN не запускается','VPN не подключается','VPN подключён, но корпоративные ресурсы недоступны','Нужно установить программу','Не печатает принтер','Не работает Wi-Fi','Не работает проводная сеть','Компьютер не включается']

@pytest.mark.parametrize('article,query',list(zip(ARTICLES,QUERIES)),ids=[a['article_id'] for a in ARTICLES])
def test_full_chain(tmp_path,article,query):
    kb=article['article_id']; calls=[]
    def upstream(request):
        body=json.loads(request.content); calls.append(body)
        assert body['sources']==[kb+'.md']
        return httpx.Response(200,json=dict(query=body['query'],answer='unused',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':kb+'.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        url='/sessions/'+c.post('/sessions',json={'user_id':'f4c'}).json()['id']
        def send(q):
            r=c.post(url+'/messages',json={'query':q}); assert r.status_code==200,r.text
        send(query)
        seen=set()
        for _ in range(10):
            status=c.get(url).json()['status']; case=c.get(url+'/diagnostic-case').json()
            assert (case['category'],case['subcategory'])==(article['category'],article['subcategory'])
            if status=='ticket_draft_ready': break
            assert status=='awaiting_result',case
            pending=next(a for a in case['actions'] if a['status']=='suggested')
            assert pending['action_id'] not in seen
            seen.add(pending['action_id'])
            send('Нет' if kb=='KB-005' else 'Не отображается' if pending.get('action_type')=='information' else 'Не помогло')
        else: pytest.fail('No terminal state')
        draft=c.get(url+'/ticket-draft').json()
        assert draft['kb_article']==kb
        assert draft['assigned_group']==article['support_group']
        assert draft['resolution']=='not_resolved'
        assert len(calls)==(0 if kb in {'KB-002','KB-005','KB-012'} else 1)
        assert c.post(url+'/ticket-draft').json()['ticket_id']==draft['ticket_id']

@pytest.mark.parametrize('status_code',[503,504])
def test_retry_same_session(tmp_path,status_code):
    calls=[]
    def upstream(request):
        body=json.loads(request.content); calls.append(body)
        if len(calls)==1: return httpx.Response(status_code,json={'detail':'unavailable'})
        return httpx.Response(200,json=dict(query=body['query'],answer='unused',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':'KB-010.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        url='/sessions/'+c.post('/sessions',json={'user_id':'f4c'}).json()['id']
        for q in ['VPN не подключается','VPN не подключается']:
            assert c.post(url+'/messages',json={'query':q}).status_code==200
        assert c.get(url).json()['status']=='awaiting_result'
        assert len(c.get(url+'/diagnostic-case').json()['actions'])==1
        assert len(calls)==2
