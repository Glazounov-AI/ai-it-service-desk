"""Persistent diagnostic evidence; classification is a hypothesis, not a fact."""
from typing import Literal
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    message_id: int
    text: str


class DiagnosticAction(BaseModel):
    action_id: str
    instruction: str
    status: Literal['suggested', 'completed'] = 'suggested'
    evidence_message_id: int | None = None
    result: str | None = None


class DiagnosticCase(BaseModel):
    session_id: str
    revision: int = 0
    category: str | None = None
    subcategory: str | None = None
    issue_summary: str | None = None
    confirmed_facts: list[Evidence] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    actions: list[DiagnosticAction] = Field(default_factory=list)
    kb_article_ids: list[str] = Field(default_factory=list)
    resolution: Literal['unknown', 'resolved', 'not_resolved'] = 'unknown'
    support_group: str | None = None
    priority: str | None = None
    escalation_reason: str | None = None
    created_at: str
    updated_at: str


def observe(case, message_id, text, classification):
    """Keep verbatim user evidence, never infer completed actions from prose.

    Evidence means a user report, not independently verified technical truth.
    """
    if classification.safety_flags or classification.domain == 'out_of_scope':
        return case
    if any(e.message_id == message_id for e in case.confirmed_facts):
        return case
    case = case.model_copy(deep=True)
    case.confirmed_facts.append(Evidence(message_id=message_id, text=text))
    if classification.domain == 'it_support':
        if case.issue_summary is None:
            case.issue_summary = text
        if classification.category:
            if case.category != classification.category:
                case.subcategory = None
                case.priority = None
            case.category = classification.category
            if classification.subcategory and not classification.needs_clarification:
                case.subcategory = classification.subcategory
                case.priority = classification.priority
        if classification.needs_clarification:
            case.missing_information = [classification.clarification_question or 'Уточните проблему.']
        else:
            case.missing_information = []
    return case
