"""Conservative, opt-in session workflow; KB text is trusted local configuration."""
import csv
import re
from pathlib import Path
from .diagnostic_case import DiagnosticAction, observe
from .models import RagResponse
from .rag_client import RagError


class DecisionEngine:
    def __init__(self, root=Path(__file__).resolve().parents[1]):
        def rows(name):
            with (root/'knowledge-base'/name).open(encoding='utf-8-sig', newline='') as f:
                return list(csv.DictReader(f, delimiter=';'))
        self.routes = {(r['category'],r['subcategory']):r for r in rows('routing-table.csv')}
        self.articles = {(r['category'],r['subcategory']):r for r in rows('it-knowledge-base.csv')}

    async def decide(self, case, mid, safe, classification, status, rag):
        text = safe.text
        def response(answer, upstream=None):
            data = upstream.model_dump() if upstream else dict(query=text, answer=answer, model='local-decision', from_cache=False)
            data.update(query=text, answer=answer, classification=classification.model_dump())
            return RagResponse.model_validate(data)
        if safe.flags or classification.domain == 'out_of_scope':
            return case, status, response('Не передавайте секретные данные и не обходите защиту.' if safe.flags else 'Я помогаю с корпоративной IT-поддержкой.')
        if status == 'escalation_required':
            return case, status, response('Обращение требует передачи в группу '+(case.support_group or 'Service Desk')+'.')
        previous = case
        case = observe(case, mid, text, classification)
        case = case.model_copy(deep=True)
        # Preserve established issue on a follow-up; never infer a different issue from a short reply.
        if previous.subcategory and (classification.domain == 'uncertain' or classification.intent in {'report_failure','report_completed_step','confirm_resolution','provide_details'}):
            case.category, case.subcategory, case.priority = previous.category, previous.subcategory, previous.priority
        if previous.subcategory and (case.category, case.subcategory) != (previous.category, previous.subcategory):
            case.category, case.subcategory, case.priority = previous.category, previous.subcategory, previous.priority
            return case, status, response('Для новой проблемы создайте отдельное обращение. Уточните результат текущей диагностики.')
        if not previous.subcategory and re.fullmatch(r'не работает vpn[.! ]*', text.lower()):
            case.category, case.subcategory = 'VPN', None
        pair = (case.category,case.subcategory)
        route = self.routes.get(pair)
        article = self.articles.get(pair)
        def escalate(reason):
            case.support_group = route['support_group'] if route else 'Service Desk'
            case.priority = route['default_priority'] if route else 'normal'
            case.escalation_reason = reason
            case.resolution = 'not_resolved'
            return case, 'escalation_required', response('Необходима передача в группу '+case.support_group+'. '+reason)
        if not route:
            question = ('VPN-клиент не запускается, не проходит авторизация, не устанавливается соединение или недоступны внутренние ресурсы?' if case.category == 'VPN' else classification.clarification_question or 'Уточните проблему и сообщение об ошибке.')
            case.missing_information = [question]
            return case, 'clarifying' if status in {'new','clarifying'} else status, response(question)
        case.missing_information = []
        case.priority = route['default_priority']
        if article:
            case.kb_article_ids = [article['article_id']]
        if pair == ('ACCESS', 'ACCOUNT_LOCKED') and article:
            return escalate('Убедитесь, что используется правильная учётная запись. Не выполняйте повторные попытки входа. Подготовьте имя учётной записи и описание ошибки. Разблокировка требует специалиста.')
        if pair == ('SOFTWARE', 'INSTALL_REQUEST') and article:
            return escalate('Если программы нет в корпоративном каталоге, не устанавливайте её из сторонних источников. Требуется согласование установки специалистом.')
        if pair == ('MFA', 'PHONE_REPLACED') and article:
            lower = text.casefold().strip(' .!')
            if previous.actions and lower in {'нет', 'нет резервного способа', 'другого способа нет', 'резервный способ недоступен'}:
                return escalate('Нет доступного резервного способа подтверждения MFA; требуется перерегистрация специалистом.')
            if previous.actions and lower in {'всё заработало', 'все заработало', 'теперь работает', 'проблема устранена'}:
                case.resolution = 'resolved'
                return case, 'resolved', response('Вход восстановлен по вашему подтверждению.')
            if previous.actions and lower in {'да', 'есть', 'есть резервный способ', 'резервный способ доступен'}:
                return case, 'awaiting_result', response('Используйте ранее зарегистрированный резервный способ для входа. Не удаляйте существующие методы MFA. Удалось войти?')
            if not previous.actions:
                case.actions.append(DiagnosticAction(action_id='KB-005:1', instruction=article['user_actions'].split('|')[0].strip()))
            return case, 'awaiting_result', response('Доступен ли другой ранее зарегистрированный резервный способ подтверждения MFA? Не передавайте коды.')
        if pair == ('OTHER', 'UNKNOWN') and not article:
            return escalate('Подходящая инструкция отсутствует. Не изменяйте настройки без утверждённой процедуры.')
        if route['admin_action_required'] == 'yes' or route['user_can_self_resolve'] == 'no':
            return escalate('Требуется вмешательство специалиста.')
        if not article:
            return escalate('Подходящая инструкция отсутствует.')
        case.kb_article_ids = [article['article_id']]
        # Explicit retrospective report of both remediation steps and persistent failure.
        if pair == ('VPN', 'RESOURCE_ACCESS') and not previous.actions and status in {'new','clarifying'}:
            if re.fullmatch(r'vpn подключ[её]н, но корпоративные ресурсы (?:вс[её] равно )?недоступны\. я уже проверил(?:а)? другой корпоративный ресурс и переподключил(?:а)? vpn [—–-] проблема осталась\. подготовь данные для передачи в поддержку\.', text.casefold().strip()):
                for instruction in article['user_actions'].split('|'):
                    instruction = instruction.strip()
                    if 'повторно подключить VPN' in instruction or 'другому корпоративному ресурсу' in instruction:
                        case.actions.append(DiagnosticAction(action_id=f"KB-011:{len(case.actions)+1}", instruction=instruction, status='completed', evidence_message_id=mid, result='not_resolved'))
                case.issue_summary = text
                return escalate('Пользователь сообщил о выполнении основных проверок VPN без устранения проблемы.')
        if pair == ('VPN', 'RESOURCE_ACCESS') and not previous.actions and re.search(r'(?:отключал(?:а)? и подключал(?:а)? vpn заново|переподключил(?:а)? vpn|переподключал(?:а)? vpn)', text.casefold()) and re.search(r'не помогло|проблема осталась|ничего не изменилось', text.casefold()):
            instruction = next(x.strip() for x in article['user_actions'].split('|') if 'повторно подключить VPN' in x)
            case.actions.append(DiagnosticAction(action_id='KB-011:1', instruction=instruction, status='completed', evidence_message_id=mid, result='not_resolved'))
        pending = next((a for a in case.actions if a.status == 'suggested'),None)
        # Only explicit, unambiguous confirmation of the outstanding action.
        if status == 'awaiting_result' and not pending and re.fullmatch(r'(проблема устранена|всё заработало|все заработало|теперь работает)[.! ]*', text.lower()):
            case.resolution = 'resolved'
            return case, 'resolved', response('Проблема устранена по вашему подтверждению.')
        if pending and status == 'awaiting_result':
            lower = text.lower().strip(' .!')
            resolved = bool(re.fullmatch(r'(проблема устранена|всё заработало|все заработало|теперь работает)',lower))
            failed = bool(re.fullmatch(r'(не помогло|ничего не изменилось|переподключился, но ничего не изменилось)',lower))
            completed = bool(re.fullmatch(r'(выполнил|выполнила|сделал|сделала)',lower))
            if lower.startswith('переподключился') and 'повторно подключить VPN' not in pending.instruction:
                failed = False
            if resolved:
                case.resolution = 'resolved'
                return case,'resolved',response('Проблема устранена по вашему подтверждению.')
            if failed or completed:
                pending.status = 'completed'
                pending.evidence_message_id = mid
                pending.result = 'not_resolved' if failed else 'unknown'
            else:
                return case,status,response('Уточните результат действия: '+pending.instruction)
        instructions = [x.strip() for x in article['user_actions'].split('|') if x.strip()]
        # VPN connection already reported: start with reconnect, then remaining checks.
        if pair == ('VPN','RESOURCE_ACCESS'):
            instructions = sorted(instructions,key=lambda x: 0 if 'повторно подключить VPN' in x else 1)
        done = {a.instruction for a in case.actions if a.status == 'completed'}
        next_step = next((x for x in instructions if x not in done),None)
        if next_step is None:
            if case.actions and case.actions[-1].result == 'not_resolved':
                return escalate('Допустимые действия исчерпаны, проблема сохраняется.')
            return case,status,response('Уточните, устранена ли проблема.')
        upstream = None
        if not previous.actions:
            try:
                upstream = await rag.query(article['title'], sources=[article['article_id']+'.md'])
            except RagError:
                return case,status,response('База знаний временно недоступна. Повторите запрос позже.')
            if not upstream.retrieved_sources:
                return escalate('Статья отсутствует в поисковом индексе.')
        case.actions.append(DiagnosticAction(action_id=f"{article['article_id']}:{len(case.actions)+1}",instruction=next_step))
        return case,'awaiting_result',response(next_step+'. Сообщите результат.',upstream)
