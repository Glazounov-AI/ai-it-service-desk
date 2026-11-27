from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings


def test_ui_assets(tmp_path):
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db')))) as c:
        r=c.get('/')
        assert r.status_code==200 and 'AI IT Service Desk' in r.text
        assert r.headers['cache-control']=='no-store'
        for name in ('app.js','style.css'):
            assert c.get('/ui-assets/'+name).status_code==200
        assert c.get('/ui-assets/missing.js').status_code==404
        assert '/' not in c.get('/openapi.json').json()['paths']
        assert c.get('/health').json()['status']=='ok'


def test_ui_session_contract(tmp_path):
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True))) as c:
        sid=c.post('/sessions',json={'user_id':'local-web'}).json()['id']
        path='/sessions/'+sid
        assert c.post(path+'/messages',json={'query':'Не работает VPN.'}).status_code==200
        assert c.get(path).json()['status']=='clarifying'
        assert len(c.get(path+'/messages').json())==2
        assert c.post(path+'/close').status_code==200
        assert c.post(path+'/messages',json={'query':'Нет'}).status_code==409
