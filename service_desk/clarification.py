"""Resolve explicit answers to a pending diagnostic question without guessing."""
import re

OPTIONS = {
    'VPN': {
        'CLIENT_START': r'(?:vpn[- ]?клиент )?не запускается|запуск|не открывается',
        'AUTHENTICATION': r'(?:не проходит |ошибка )?(?:авторизация|аутентификация)|не удаётся авторизоваться',
        'CONNECTION': r'(?:не устанавливается соединение|соединение не устанавливается|не подключается|подключение|соединение)',
        'RESOURCE_ACCESS': r'(?:недоступны (?:внутренние|корпоративные) ресурсы|(?:внутренние|корпоративные) ресурсы недоступны|не открываются (?:внутренние|корпоративные) ресурсы)',
    },
    'EMAIL': {
        'OUTLOOK_START': r'(?:outlook )?не запускается|не открывается|запуск',
        'SEND_RECEIVE': r'не (?:отправляются|принимаются|приходят|получаются) письма|не отправляются и не принимаются письма|отправка и получение',
    },
    'NETWORK': {
        'LAN': r'lan|кабель|по кабелю|проводная сеть|проводное подключение',
        'WIFI': r'wi[- ]?fi|вай[- ]?фай|беспроводная сеть',
    },
}


def resolve(safe, baseline, case, status, classifier):
    if safe.flags or baseline.domain == 'out_of_scope' or status != 'clarifying' or case.subcategory or not case.missing_information:
        return None
    q = safe.text.casefold().strip(' .!?')
    if case.category == 'NETWORK' and q == 'vpn':
        return baseline.model_copy(update=dict(domain='it_support', category='VPN', subcategory=None, priority=None, intent='provide_details', confidence=1.0, method='rules', needs_clarification=True, clarification_question='VPN-клиент не запускается, не проходит авторизация, не устанавливается соединение или недоступны внутренние ресурсы?', kb_available=None, generation_reason='contextual_clarification'))
    matches = [(case.category, sub) for sub, pattern in OPTIONS.get(case.category, {}).items() if re.fullmatch(pattern, q)]
    if len(matches) != 1 or matches[0] not in classifier.pairs:
        return None
    pair = matches[0]
    return baseline.model_copy(update=dict(domain='it_support', category=pair[0], subcategory=pair[1], priority=classifier.pairs[pair], intent='provide_details', confidence=1.0, method='rules', needs_clarification=False, clarification_question=None, kb_available=pair in classifier.kb, generation_reason='contextual_clarification'))
