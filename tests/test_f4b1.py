import csv
import json
import httpx
import pytest
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings
from service_desk.action_results import kind, interpret, TYPES

@pytest.mark.parametrize('article', list(csv.DictReader(open('knowledge-base/it-knowledge-base.csv', encoding='utf-8-sig'), delimiter=';')))
def test_all_article_types(article):
    steps = [x.strip() for x in article['user_actions'].split('|') if x.strip()]
    assert len(steps) == len(TYPES[article['article_id']])
    for step in steps:
        t = kind(article, step)
        assert interpret(t, 'Проблема устранена') == 'resolved'
        if t == 'information':
            assert interpret(t, 'Не помогло') == 'information_unavailable'
            assert interpret(t, 'Да') is None

@pytest.mark.parametrize('reply,outcome', [('не отображается','information_unavailable'),('Текст ошибки: ошибка TLS-рукопожатия','information_reported'),('Не помогло','information_unavailable'),('Да',None)])
def test_vpn_information(tmp_path, reply, outcome):
    def upstream(request):
        body=json.loads(request.content)
        assert body['sources']==['KB-010.md']
        return httpx.Response(200,json=dict(query=body['query'],answer='unused',model='test',from_cache=False,strategy='targeted',retrieved_sources=[{'source':'KB-010.md'}]))
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db'),managed_diagnostics=True),httpx.MockTransport(upstream))) as c:
        url='/sessions/'+c.post('/sessions',json={'user_id':'test'}).json()['id']
        def send(q):
            r=c.post(url+'/messages',json={'query':q}); assert r.status_code==200,r.text
        for q in ['Не работает VPN','Не устанавливается соединение','Не помогло','Не помогло',reply]: send(q)
        if outcome is None:
            assert c.get(url).json()['status']=='awaiting_result'
            send(reply)
        assert c.get(url).json()['status']=='ticket_draft_ready'
        draft=c.get(url+'/ticket-draft').json()
        a=draft['troubleshooting_actions'][-1]
        assert a['result']==outcome
        assert a['status']==('completed' if outcome else 'suggested')
        assert any(e['text']==reply for e in draft['confirmed_facts'])
        assert draft['is_complete']==(outcome=='information_reported')
