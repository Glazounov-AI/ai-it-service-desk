import httpx
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

TS022 = 'VPN подключён, но корпоративные ресурсы всё равно недоступны. Я уже проверил другой корпоративный ресурс и переподключил VPN — проблема осталась. Подготовь данные для передачи в поддержку.'


def test_ts022_and_persistence(tmp_path):
    settings = Settings(db_path=str(tmp_path/'db'), managed_diagnostics=True)
    def upstream(request):
        raise AssertionError('Unexpected upstream call')
    transport = httpx.MockTransport(upstream)
    with TestClient(create_app(settings, transport)) as c:
        sid = c.post('/sessions',json={'user_id':'test'}).json()['id']
        url = f'/sessions/{sid}'
        assert c.get(url+'/ticket-draft').status_code == 404
        assert c.post(url+'/ticket-draft').status_code == 409
        r = c.post(url+'/messages',json={'query':TS022})
        assert r.status_code == 200, r.text
        assert c.get(url).json()['status'] == 'ticket_draft_ready'
        d = c.get(url+'/ticket-draft').json()
        assert d['assigned_group']=='Network' and d['kb_article']=='KB-011'
        assert d['troubleshooting_completed'] and not d['is_complete']
        assert len(d['troubleshooting_actions'])==2
        assert d['case_revision']==c.get(url+'/diagnostic-case').json()['revision']
        assert c.post(url+'/ticket-draft').json()==d
        assert c.post(url+'/messages',json={'query':TS022}).status_code==409
        other=c.post('/sessions',json={'user_id':'other'}).json()['id']
        assert c.get(f'/sessions/{other}/ticket-draft').status_code==404
    with TestClient(create_app(settings, transport)) as c:
        assert c.get(url+'/ticket-draft').json()==d
        assert c.post(url+'/ticket-draft').json()==d


def test_admin_draft(tmp_path):
    def upstream(request):
        raise AssertionError('Unexpected upstream call')
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        sid=c.post('/sessions',json={'user_id':'test'}).json()['id']
        url=f'/sessions/{sid}'
        assert c.post(url+'/messages',json={'query':'Дайте мне права администратора.'}).status_code==200
        d=c.get(url+'/ticket-draft').json()
        assert d['assigned_group']=='Identity & Access' and d['kb_article'] is None
        assert not d['troubleshooting_completed']
