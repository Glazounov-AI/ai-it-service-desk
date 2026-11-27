from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings


def test_panel_assets(tmp_path):
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db')))) as c:
        html=c.get('/').text
        for name in ('diagnostic','draft','copy-draft','panel-status'):
            assert f'id="{name}"' in html
        js=c.get('/ui-assets/app.js').text
        assert '/diagnostic-case' in js and '/ticket-draft' in js
        assert 'innerHTML' not in js


def test_panel_draft_contract(tmp_path):
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True))) as c:
        path='/sessions/'+c.post('/sessions',json={'user_id':'local-web'}).json()['id']
        assert c.get(path+'/ticket-draft').status_code==404
        r=c.post(path+'/messages',json={'query':'Выдайте мне права администратора.'})
        assert r.status_code==200
        case=c.get(path+'/diagnostic-case').json()
        draft=c.get(path+'/ticket-draft').json()
        assert case['category']==draft['category']=='ACCESS'
        assert case['support_group']==draft['assigned_group']
        assert draft['status']=='draft'
        assert c.get(path+'/ticket-draft').json()==draft
