import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

@pytest.fixture
def session(tmp_path):
    def upstream(request):
        body=json.loads(request.content)
        assert body['sources']==['KB-011.md']
        return httpx.Response(200,json=dict(query=body['query'],answer='unused',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':'KB-011.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        url='/sessions/'+c.post('/sessions',json={'user_id':'test'}).json()['id']
        def send(q):
            r=c.post(url+'/messages',json={'query':q}); assert r.status_code==200,r.text; return r.json()
        yield c,url,send

@pytest.mark.parametrize('q', ['Outlook не работает.','У меня нет сети.','При подключении появляется ошибка 720.','Где мне изменить эту настройку Windows?','Не работает почта.','Ошибка 123.'])
def test_clarify(session,q):
    c,u,send=session
    r=send(q)
    assert r['classification']['needs_clarification'] and '?' in r['answer']
    assert c.get(u).json()['status']=='clarifying'
    assert c.get(u+'/ticket-draft').status_code==404

@pytest.mark.parametrize('q,kb,group,phrase', [('Пишет, что моя учётная запись заблокирована. Разблокируй её.','KB-002','Identity & Access','Не выполняйте повторные'),('Мне нужен графический редактор, но его нет в корпоративном каталоге. Как его установить?','KB-012','Workplace','сторонних источников'),('После обновления BIOS ноутбук стал очень долго загружаться. Что изменить в BIOS?',None,'Service Desk','Подходящая инструкция отсутствует')])
def test_escalation(session,q,kb,group,phrase):
    c,u,send=session
    assert phrase in send(q)['answer']
    d=c.get(u+'/ticket-draft').json()
    assert d['kb_article']==kb and d['assigned_group']==group

@pytest.mark.parametrize('available',[True,False])
def test_mfa(session,available):
    c,u,send=session
    assert '?' in send('Поменял телефон. Старого уже нет, теперь не могу подтвердить MFA.')['answer']
    assert c.get(u+'/ticket-draft').status_code==404
    send('Да' if available else 'Нет')
    if available:
        assert c.get(u).json()['status']=='awaiting_result'
        send('Всё заработало.')
        assert c.get(u).json()['status']=='resolved'
    else:
        assert c.get(u+'/ticket-draft').json()['kb_article']=='KB-005'

def test_reconnect(session):
    c,u,send=session
    r=send('VPN подключён, но внутренние ресурсы не открываются. Я уже отключал и подключал VPN заново — не помогло.')
    assert 'повторно подключить VPN' not in r['answer']
    a=c.get(u+'/diagnostic-case').json()['actions']
    assert a[0]['status']=='completed' and a[0]['evidence_message_id'] and a[1]['status']=='suggested'
