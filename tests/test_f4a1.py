import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings

@pytest.mark.parametrize('first,reply,category,sub,kb', [
    ('Не работает VPN','не устанавливается соединение','VPN','CONNECTION','KB-010'),
    ('Не работает VPN','не запускается','VPN','CLIENT_START','KB-009'),
    ('Не работает VPN','не проходит авторизация','VPN','AUTHENTICATION',None),
    ('Не работает VPN','недоступны внутренние ресурсы','VPN','RESOURCE_ACCESS','KB-011'),
    ('Outlook не работает','не запускается','EMAIL','OUTLOOK_START','KB-007'),
    ('Outlook не работает','не отправляются письма','EMAIL','SEND_RECEIVE','KB-008'),
    ('Нет сети','LAN','NETWORK','LAN','KB-015'),
    ('Нет сети','Wi-Fi','NETWORK','WIFI','KB-014'),
    ('Нет сети','VPN','VPN',None,None),
])
def test_contextual_reply(tmp_path,first,reply,category,sub,kb):
    def upstream(request):
        body=json.loads(request.content)
        assert kb and body['sources']==[kb+'.md']
        return httpx.Response(200,json=dict(query=body['query'],answer='unused',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':kb+'.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        url='/sessions/'+c.post('/sessions',json={'user_id':'test'}).json()['id']
        assert c.post(url+'/messages',json={'query':first}).status_code==200
        assert c.get(url).json()['status']=='clarifying'
        r=c.post(url+'/messages',json={'query':reply}); assert r.status_code==200,r.text
        cl=r.json()['classification']; assert (cl['category'],cl['subcategory'])==(category,sub)
        assert cl['generation_reason']=='contextual_clarification'
        assert c.get(url).json()['status']==('awaiting_result' if kb else 'ticket_draft_ready' if sub else 'clarifying')
        assert c.get(url+'/diagnostic-case').json()['confirmed_facts'][-1]['text']==reply
