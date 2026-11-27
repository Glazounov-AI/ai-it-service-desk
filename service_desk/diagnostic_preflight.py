"""Conservative rules before paid classification in managed sessions."""
import re


def preflight(safe, baseline, case, status):
    if safe.flags:
        return None
    q = safe.text.casefold().strip(' .!')
    if not case.subcategory and status in {'new', 'clarifying'}:
        vague = [
            (r'(?:outlook|почта) не работает|не работает (?:outlook|почта)', 'EMAIL', 'Outlook не запускается или не отправляются и не принимаются письма?'),
            (r'(?:у меня )?нет сети|пропала сеть|не работает сеть', 'NETWORK', 'Какое подключение используется: LAN, Wi-Fi или VPN?'),
            (r'(?:при подключении )?(?:появляется )?ошибка \d+', None, 'В каком приложении или системе появляется ошибка?'),
            (r'где (?:мне )?изменить (?:эту )?настройку windows', None, 'Какую настройку нужно изменить и какая версия Windows: Windows 10 или Windows 11?'),
        ]
        for pattern, category, question in vague:
            if re.fullmatch(pattern, q):
                return baseline.model_copy(update=dict(domain='it_support', category=category, subcategory=None, priority=None, intent='report_issue', confidence=1.0, method='rules', needs_clarification=True, clarification_question=question, kb_available=None, generation_reason='diagnostic_preflight'))
        if re.search(r'\bbios\b', q) and re.search(r'обновлен|обновлён|настрой|измен|загруз', q):
            return baseline.model_copy(update=dict(domain='it_support', category='OTHER', subcategory='UNKNOWN', priority='normal', intent='report_issue', confidence=1.0, method='rules', needs_clarification=False, clarification_question=None, kb_available=False, generation_reason='diagnostic_preflight'))
    if case.category == 'MFA' and case.subcategory == 'PHONE_REPLACED' and status == 'awaiting_result' and q in {'да', 'нет', 'есть', 'нет резервного способа', 'другого способа нет', 'резервный способ недоступен', 'есть резервный способ', 'резервный способ доступен', 'всё заработало', 'все заработало', 'теперь работает', 'проблема устранена'}:
        return baseline.model_copy(update=dict(domain='it_support', category='MFA', subcategory='PHONE_REPLACED', priority=case.priority, intent='provide_details', confidence=1.0, method='rules', needs_clarification=False, clarification_question=None, kb_available=True, generation_reason='diagnostic_preflight'))
    if status == 'awaiting_result' and case.category and case.subcategory and case.subcategory != 'PHONE_REPLACED' and baseline.domain != 'out_of_scope':
        from .action_results import interpret_pending
        pending = next((a for a in case.actions if a.status == 'suggested'), None)
        outcome = interpret_pending(pending, safe.text) if pending and pending.action_type else None
        if outcome in {'information_reported','information_unavailable','check_positive','check_negative','not_resolved'}:
            return baseline.model_copy(update=dict(domain='it_support', category=case.category, subcategory=case.subcategory, priority=case.priority, intent='report_failure' if outcome == 'not_resolved' else 'provide_details', confidence=1.0, method='rules', needs_clarification=False, clarification_question=None, kb_available=True, generation_reason='diagnostic_preflight'))
    if baseline.domain == 'out_of_scope':
        return None
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
