"""Typed results for the current trusted KB instructions; no free-text inference."""
import re

# Ordered types correspond to the versioned CSV instructions.
TYPES = {
 'KB-001': 'rrrrr', 'KB-002': 'cci', 'KB-003': 'crc',
 'KB-004': 'ccrr', 'KB-005': 'crc', 'KB-006': 'crcr',
 'KB-007': 'rrr', 'KB-008': 'cccr', 'KB-009': 'crrr',
 'KB-010': 'cri', 'KB-011': 'ccri', 'KB-012': 'crc',
 'KB-013': 'cccrr', 'KB-014': 'ccrr', 'KB-015': 'ccrc',
 'KB-016': 'cccrri',
}

def kind(article, instruction):
    steps = [x.strip() for x in article['user_actions'].split('|') if x.strip()]
    return {'c':'check','r':'remediation','i':'information'}[TYPES[article['article_id']][steps.index(instruction)]]


def interpret(action_type, text):
    q = text.casefold().strip(' .!')
    if q in {'проблема устранена','всё заработало','все заработало','теперь работает'}:
        return 'resolved'
    if action_type == 'information':
        if q in {'не отображается','нет ошибки','ошибки нет','не знаю','не могу определить','нет информации','не отображаются','не помогло','ничего не изменилось','выполнил','выполнила','сделал','сделала'}:
            return 'information_unavailable'
        if re.fullmatch(r'(?:текст ошибки|код ошибки|ошибка|код|ресурс|ресурсы|индикация|сообщение об ошибке)\s*[:—-]\s*\S.*', q) or re.fullmatch(r'(?:ошибка\s+)?(?:0x[0-9a-f]+|\d{3,5})',q):
            return 'information_reported'
        return None
    if q in {'не помогло','ничего не изменилось','переподключился, но ничего не изменилось'}:
        return 'not_resolved'
    if q in {'выполнил','выполнила','сделал','сделала'}:
        return 'unknown'
    if action_type == 'check':
        if q in {'да','есть','доступен','доступна','работает','включён','включен','подключён','подключен','connected'}:
            return 'check_positive'
        if q in {'нет','не работает','недоступен','недоступна','не подключен','не подключён','не включен','не включён','не отображается'}:
            return 'check_negative'
    return None
