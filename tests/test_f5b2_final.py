import httpx
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings
from service_desk.action_results import interpret_pending
from service_desk.diagnostic_case import DiagnosticAction


def test_natural_vpn_chain_without_upstream(tmp_path):
    calls=[]
    def handler(req):
        calls.append(req.url.path)
        return httpx.Response(503)
    settings=Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True,diagnostic_lookup='local',generation_enabled=True,generation_key='test')
    with TestClient(create_app(settings,httpx.MockTransport(handler))) as c:
        sid=c.post('/sessions',json={'user_id':'test'}).json()['id']
        for text in ['VPN подключён, но корпоративные ресурсы недоступны.','Переподключил VPN, не помогло.','VPN показывает Connected.','Другой корпоративный ресурс тоже недоступен.','Недоступны корпоративный портал и файловый сервер.']:
            r=c.post(f'/sessions/{sid}/messages',json={'query':text})
            assert r.status_code==200, r.text
            assert r.json()['strategy']=='local'
        draft=c.get(f'/sessions/{sid}/ticket-draft').json()
        assert draft['assigned_group']=='Network'
        assert draft['troubleshooting_completed']
        assert [a['result'] for a in draft['troubleshooting_actions']]==['not_resolved','check_positive','check_negative','information_reported']
        assert calls==[]


def test_wrong_action_not_confirmed():
    a=DiagnosticAction(action_id='test',instruction='Проверить доступ к другому корпоративному ресурсу',action_type='check')
    assert interpret_pending(a,'Переподключил VPN, не помогло.') is None
    assert interpret_pending(a,'VPN показывает Connected.') is None
