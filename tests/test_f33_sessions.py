import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings
from service_desk.storage import SQLiteRepository, SessionError


def handler(request):
    return httpx.Response(200, json={'query':json.loads(request.content)['query'], 'answer':'Ответ', 'model':'test','from_cache':False})


def client(path, upstream=handler):
    return TestClient(create_app(Settings(db_path=str(path)), httpx.MockTransport(upstream)))


def create(c):
    r = c.post('/sessions', json={'user_id':'test'})
    assert r.status_code == 201
    return r.json()['id']


def test_persistence_and_isolation(tmp_path):
    path = tmp_path/'db.sqlite'
    with client(path) as c:
        a,b = create(c),create(c)
        assert a != b
        assert c.post(f'/sessions/{a}/messages',json={'query':'VPN'}).status_code == 200
        assert c.get(f'/sessions/{b}/messages').json() == []
    with client(path) as c:
        rows = c.get(f'/sessions/{a}/messages').json()
        assert [r['role'] for r in rows] == ['user','assistant']
        assert rows[1]['metadata']['model'] == 'test'
        assert c.get(f'/sessions/{a}').json()['status'] == 'new'


def test_failure(tmp_path):
    with client(tmp_path/'db',lambda r:httpx.Response(504)) as c:
        a = create(c)
        assert c.post(f'/sessions/{a}/messages',json={'query':'VPN'}).status_code == 504
        assert [r['role'] for r in c.get(f'/sessions/{a}/messages').json()] == ['user']


def test_close(tmp_path):
    with client(tmp_path/'db') as c:
        a = create(c)
        assert c.post(f'/sessions/{a}/close').json()['closed_at']
        assert c.post(f'/sessions/{a}/messages',json={'query':'VPN'}).status_code == 409
        assert c.post(f'/sessions/{a}/close').status_code == 409


@pytest.mark.parametrize('suffix,method', [('', 'GET'),('/messages','GET'),('/messages','POST'),('/close','POST')])
def test_unknown(tmp_path,suffix,method):
    with client(tmp_path/'db') as c:
        kwargs = {'json':{'query':'VPN'}} if method == 'POST' else {}
        assert c.request(method,'/sessions/missing'+suffix,**kwargs).status_code == 404


def test_transitions(tmp_path):
    repo = SQLiteRepository(tmp_path/'db')
    sid = repo.create('test')['id']
    with pytest.raises(SessionError):
        repo.transition(sid,'resolved')
    for state in ['clarifying','troubleshooting','awaiting_result','resolved','closed']:
        assert repo.transition(sid,state)['status'] == state


def test_validation(tmp_path):
    with client(tmp_path/'db') as c:
        assert c.post('/sessions',json={'user_id':' '}).status_code == 422
        a = create(c)
        assert c.post(f'/sessions/{a}/messages',json={'query':' '}).status_code == 422
        assert c.get(f'/sessions/{a}/messages').json() == []


def test_exclusive(tmp_path):
    from service_desk.sessions import SessionService
    repo = SQLiteRepository(tmp_path/'db')
    service = SessionService(repo, None)
    sid = repo.create('test')['id']
    with service.exclusive(sid):
        with pytest.raises(SessionError):
            service.close(sid)
    assert service.close(sid)['status'] == 'closed'
