"""Deterministic draft construction; no persistence or external submission."""
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel
from .diagnostic_case import DiagnosticCase, Evidence, DiagnosticAction
from .decision import DecisionEngine
from .safety import SafetyFilter


class TicketDraft(BaseModel):
    ticket_id: str
    session_id: str
    user_id: str
    title: str
    issue_summary: str
    category: str
    subcategory: str
    request_type: str
    priority: str
    assigned_group: str
    kb_article: str | None
    kb_article_ids: list[str]
    confirmed_facts: list[Evidence]
    troubleshooting_actions: list[DiagnosticAction]
    troubleshooting_completed: bool
    resolution: Literal['not_resolved'] = 'not_resolved'
    action: Literal['escalate'] = 'escalate'
    escalation_reason: str
    missing_information: list[str]
    is_complete: bool
    case_revision: int
    status: Literal['draft'] = 'draft'
    created_at: str
    updated_at: str


class TicketDraftBuilder:
    def __init__(self, taxonomy=None, safety=None):
        self.taxonomy = taxonomy or DecisionEngine()
        self.safety = safety or SafetyFilter()

    def build(self, case: DiagnosticCase, session: dict) -> TicketDraft:
        if session['id'] != case.session_id or session['status'] != 'escalation_required':
            raise ValueError('Draft requires matching escalated session')
        route = self.taxonomy.routes.get((case.category, case.subcategory))
        if not route or case.resolution != 'not_resolved' or not case.escalation_reason or not case.issue_summary:
            raise ValueError('Incomplete escalation state')
        if (case.support_group, case.priority) != (route['support_group'], route['default_priority']):
            raise ValueError('Escalation routing mismatch')
        article = self.taxonomy.articles.get((case.category, case.subcategory))
        if case.kb_article_ids and (not article or case.kb_article_ids != [article['article_id']]):
            raise ValueError('Invalid KB references')
        facts = {e.message_id: e for e in case.confirmed_facts}
        if len(facts) != len(case.confirmed_facts):
            raise ValueError('Duplicate evidence')
        if not any(e.text == case.issue_summary for e in facts.values()):
            raise ValueError('Issue summary lacks evidence')
        for a in case.actions:
            if a.status == 'completed' and a.evidence_message_id not in facts:
                raise ValueError('Action lacks evidence')
        missing = list(case.missing_information) + [a.instruction for a in case.actions if a.result == 'information_unavailable']
        # D18: generic completion does not establish the collected information.
        # Require a typed report for the resource collection step.
        if (case.category, case.subcategory) == ('VPN', 'RESOURCE_ACCESS') and not any(a.result == 'information_reported' and 'ресурсы недоступны' in a.instruction for a in case.actions):
            missing.append('Названия недоступных корпоративных ресурсов не подтверждены структурированными данными.')
        instructions = {x.strip() for x in article['user_actions'].split('|') if x.strip()} if article and case.kb_article_ids else set()
        completed = {a.instruction for a in case.actions if a.status == 'completed' and a.result in {'not_resolved', 'check_positive', 'check_negative', 'unknown', 'information_reported', 'information_unavailable'}}
        if (case.category, case.subcategory) == ('VPN', 'RESOURCE_ACCESS'):
            # TS-022: remediation checks, not information collection.
            instructions = {x for x in instructions if 'повторно подключить VPN' in x or 'другому корпоративному ресурсу' in x}
        stamp = datetime.now(timezone.utc).isoformat()
        data = dict(ticket_id=str(uuid4()), session_id=case.session_id, user_id=session['user_id'],
                    title=route['request_type'], issue_summary=case.issue_summary, category=case.category,
                    subcategory=case.subcategory, request_type=route['request_type'], priority=case.priority,
                    assigned_group=case.support_group, kb_article=case.kb_article_ids[0] if case.kb_article_ids else None,
                    kb_article_ids=case.kb_article_ids, confirmed_facts=case.confirmed_facts,
                    troubleshooting_actions=case.actions, troubleshooting_completed=bool(instructions) and instructions <= completed,
                    escalation_reason=case.escalation_reason, missing_information=list(dict.fromkeys(missing)),
                    is_complete=not missing, case_revision=case.revision, created_at=stamp, updated_at=stamp)
        return TicketDraft.model_validate(self.safety.clean(TicketDraft.model_validate(data).model_dump()))
