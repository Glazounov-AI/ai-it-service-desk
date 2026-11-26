import pytest
import httpx
from fastapi.testclient import TestClient
from service_desk.api import create_app
from service_desk.config import Settings
from service_desk.classification.classifier import Classifier
from service_desk.safety import SafetyFilter


@pytest.mark.parametrize('query,pair', [
    ('Outlook не запускается', ('EMAIL','OUTLOOK_START')),
    ('Не запускается VPN-клиент', ('VPN','CLIENT_START')),
    ('Не подключается VPN', ('VPN','CONNECTION')),
    ('VPN подключён, ресурсы недоступны', ('VPN','RESOURCE_ACCESS')),
    ('Не печатает принтер', ('HARDWARE','PRINTER')),
    ('Нет Wi-Fi', ('NETWORK','WIFI')),
    ('Компьютер не включается', ('HARDWARE','PC_START')),
    ('Нужны права администратора', ('ACCESS','PERMISSIONS')),
])
def test_classification(query, pair):
    result = Classifier().classify(query)
    assert (result.category, result.subcategory) == pair
    assert not result.needs_clarification


def test_ambiguity():
    assert Classifier().classify('VPN').needs_clarification
    assert Classifier().classify('VPN').subcategory is None
    assert Classifier().classify('Рецепт супа').domain == 'out_of_scope'
    assert Classifier().classify('Что делать?').domain == 'uncertain'


@pytest.mark.parametrize('query', ['Пароль: testSecret123', 'код MFA: 123456', 'token=abcdef', '-----BEGIN PRIVATE KEY-----\nabc'])
def test_safety(query):
    result = SafetyFilter().inspect(query)
    assert result.flags
    assert query not in result.text


def test_no_bare_number():
    assert not SafetyFilter().inspect('Ошибка 123456').flags


def test_session_safety(tmp_path):
    with TestClient(create_app(Settings(db_path=str(tmp_path/'db')), httpx.MockTransport(lambda r: pytest.fail('Unexpected upstream')))) as c:
        sid = c.post('/sessions',json={'user_id':'test'}).json()['id']
        path = f'/sessions/{sid}/messages'
        r = c.post(path,json={'query':'Пароль: testSecret123'})
        assert r.status_code == 200
        assert 'testSecret123' not in r.text
        assert 'testSecret123' not in c.get(path).text
        assert c.post('/consult',json={'query':'Пароль: testSecret123'}).status_code == 200
        r = c.post('/consult',json={'query':'testSecret123'*300})
        assert r.status_code == 422
        assert 'testSecret123' not in r.text
