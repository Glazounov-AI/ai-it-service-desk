import pytest
from scripts.evaluate_classification import evaluate
from service_desk.classification.classifier import Classifier
from service_desk.safety import SafetyFilter

@pytest.mark.parametrize('row', evaluate(), ids=lambda r:r['id'])
def test_original_scenario(row):
    assert row['passed'], row['checks']

@pytest.mark.parametrize('query,pair', [
 ('Не удаётся войти в корпоративную учётную запись', ('ACCESS','LOGIN_FAILED')),
 ('Проблема с профилем Outlook', ('EMAIL','PROFILE')),
 ('Нет доступа к почтовому ящику', ('EMAIL','MAILBOX_ACCESS')),
 ('Корпоративное приложение не запускается', ('SOFTWARE','APP_START')),
 ('Ошибка при работе приложения', ('SOFTWARE','APP_ERROR')),
 ('Не обновляется программное обеспечение', ('SOFTWARE','UPDATE')),
 ('Не работает мышь', ('HARDWARE','PERIPHERAL')),
 ('Нет изображения на мониторе', ('HARDWARE','DISPLAY')),
 ('Недоступен сетевой ресурс', ('NETWORK','SHARED_RESOURCE')),
 ('Неизвестная IT-проблема', ('OTHER','UNKNOWN')),
])
def test_added_pairs(query,pair):
    c=Classifier(); r=c.classify(query)
    assert (r.category,r.subcategory)==pair
    assert r.kb_available == (pair in c.kb)

def test_rule_coverage():
    c=Classifier()
    assert {pair for pair,_ in c.rules} == set(c.pairs)

@pytest.mark.parametrize('query',['Ошибка 123456','Код ошибки 123456','Не приходит код MFA'])
def test_no_false_secret(query):
    assert not SafetyFilter().inspect(query).flags

@pytest.mark.parametrize('query,secret',[('Пароль: ExampleSecret123','ExampleSecret123'),('код MFA: 123456','123456'),('token=abcdef','abcdef')])
def test_no_secret_leak(query,secret):
    assert secret not in SafetyFilter().inspect(query).text
