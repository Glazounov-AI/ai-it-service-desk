"""Conservative rules before paid classification in managed sessions."""
import re


def preflight(safe, baseline, case, status):
    if safe.flags or baseline.domain == 'out_of_scope':
        return None
    q = safe.text.casefold().strip(' .!')
    resolved = re.fullmatch(r'проблема устранена|всё заработало|все заработало|теперь работает', q)
    failed = re.fullmatch(r'не помогло|ничего не изменилось|переподключился, но ничего не изменилось', q)
    completed = re.fullmatch(r'выполнил|выполнила|сделал|сделала', q)
    if resolved or failed or completed:
        if status == 'awaiting_result' and case.category and case.subcategory and case.actions:
            return baseline.model_copy(update=dict(domain='it_support', category=case.category, subcategory=case.subcategory, priority=case.priority, intent='confirm_resolution' if resolved else 'report_failure' if failed else 'report_completed_step', confidence=1.0, method='rules', needs_clarification=False, clarification_question=None, kb_available=bool(case.kb_article_ids), generation_reason='diagnostic_preflight'))
        return baseline.model_copy(update=dict(domain='uncertain', category=None, subcategory=None, priority=None, intent='unknown', confidence=1.0, method='rules', needs_clarification=True, clarification_question='Уточните, какое устройство или сервис не работает и какое действие вы выполнили.', kb_available=None, generation_reason='diagnostic_preflight'))
    if q == 'не работает vpn' and not case.subcategory:
        return baseline.model_copy(update=dict(domain='it_support', category='VPN', subcategory=None, priority=None, intent='report_issue', confidence=1.0, method='rules', needs_clarification=True, clarification_question='VPN-клиент не запускается, не проходит авторизация, не устанавливается соединение или недоступны внутренние ресурсы?', kb_available=None, generation_reason='diagnostic_preflight'))
    return None
