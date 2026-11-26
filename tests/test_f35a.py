import pytest
from service_desk.storage import SQLiteRepository, SessionError
from service_desk.diagnostic_case import observe, Evidence
from service_desk.classification.models import Classification


def classification(**kwargs):
    return Classification(**({'domain':'it_support','category':'VPN','confidence':.9} | kwargs))


def test_persistent_evidence(tmp_path):
    path = tmp_path/'db'
    repo = SQLiteRepository(path)
    a,b = [repo.create('user')['id'] for _ in range(2)]
    mid = repo.append(a,'user','VPN не работает')
    case = observe(repo.get_case(a),mid,'VPN не работает',classification(needs_clarification=True))
    saved = repo.save_case(case)
    assert saved.revision == 1
    assert SQLiteRepository(path).get_case(a) == saved
    assert repo.get_case(b).confirmed_facts == []
    assert saved.actions == []
    with pytest.raises(SessionError):
        repo.save_case(case)


@pytest.mark.parametrize('role,other_session,text', [('assistant',False,'fact'),('user',True,'fact'),('user',False,'invented')])
def test_invalid_evidence(tmp_path,role,other_session,text):
    repo = SQLiteRepository(tmp_path/'db')
    a,b = [repo.create('user')['id'] for _ in range(2)]
    mid = repo.append(b if other_session else a,role,'fact')
    case = repo.get_case(a)
    case.confirmed_facts.append(Evidence(message_id=mid,text=text))
    with pytest.raises(SessionError):
        repo.save_case(case)


@pytest.mark.parametrize('kwargs',[{'domain':'out_of_scope'},{'safety_flags':['secret']}])
def test_ignored(tmp_path,kwargs):
    repo = SQLiteRepository(tmp_path/'db')
    sid = repo.create('user')['id']
    case = repo.get_case(sid)
    assert observe(case,1,'ignored',classification(**kwargs)) == case


def test_context_not_completion(tmp_path):
    repo = SQLiteRepository(tmp_path/'db')
    sid = repo.create('user')['id']
    case = repo.get_case(sid)
    case = observe(case,1,'VPN подключён, ресурсы недоступны',classification(subcategory='RESOURCE_ACCESS'))
    case = observe(case,2,'Переподключился',classification(domain='uncertain',category=None))
    assert case.subcategory == 'RESOURCE_ACCESS'
    assert not case.actions
    assert case.resolution == 'unknown'


def test_api_case(tmp_path):
    import httpx
    from fastapi.testclient import TestClient
    from service_desk.api import create_app
    from service_desk.config import Settings
    def upstream(request):
        return httpx.Response(200,json={'query':'VPN','answer':'Ответ','model':'test','from_cache':False})
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db')),httpx.MockTransport(upstream))) as c:
        sid = c.post('/sessions',json={'user_id':'test'}).json()['id']
        assert c.get(f'/sessions/{sid}/diagnostic-case').json()['revision'] == 0
        assert c.post(f'/sessions/{sid}/messages',json={'query':'VPN'}).status_code == 200
        assert c.get(f'/sessions/{sid}/diagnostic-case').json()['confirmed_facts'][0]['text'] == 'VPN'
        assert c.get('/sessions/missing/diagnostic-case').status_code == 404
