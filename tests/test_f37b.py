import json
import sqlite3
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

@pytest.mark.parametrize('secret,query', [('F37SyntheticPassword','Пароль: F37SyntheticPassword'),('sk-F37SyntheticToken123456','Токен: sk-F37SyntheticToken123456'),('987654','Код MFA: 987654')])
def test_secret_not_persisted(tmp_path,secret,query):
    path=tmp_path/'db'
    def upstream(request):
        raise AssertionError('Safety must be local')
    with TestClient(create_app(Settings(db_path=str(path),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        u='/sessions/'+c.post('/sessions',json={'user_id':'test'}).json()['id']
        r=c.post(u+'/messages',json={'query':query})
        assert r.status_code==200 and secret not in r.text
        assert secret not in c.get(u+'/messages').text
        assert secret not in c.get(u+'/diagnostic-case').text
    with sqlite3.connect(path) as db:
        assert secret not in '\n'.join(db.iterdump())

@pytest.mark.parametrize('status',[503,504])
def test_recovery(tmp_path,status):
    calls=[]
    def upstream(request):
        calls.append(json.loads(request.content))
        if len(calls)==1: return httpx.Response(status)
        return httpx.Response(200,json={'query':calls[-1]['query'],'answer':'unused','model':'test','from_cache':False,'strategy':'targeted','retrieved_sources':[{'source':'KB-009.md'}]})
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        u='/sessions/'+c.post('/sessions',json={'user_id':'test'}).json()['id']
        q={'query':'Не запускается VPN-клиент.'}
        assert 'временно недоступна' in c.post(u+'/messages',json=q).json()['answer']
        assert c.get(u+'/diagnostic-case').json()['actions']==[]
        assert c.post(u+'/messages',json=q).json()['strategy']=='targeted'
        assert c.get(u).json()['status']=='awaiting_result'
        assert len(c.get(u+'/messages').json())==4
        assert all(x['sources']==['KB-009.md'] for x in calls)
