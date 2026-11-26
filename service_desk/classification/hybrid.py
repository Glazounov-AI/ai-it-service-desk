import logging
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from typing import Literal
from .models import Classification
from ..rag_client import RagError


class Candidate(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    domain: Literal['it_support', 'out_of_scope', 'uncertain']
    category: str | None
    subcategory: str | None
    intent: Literal['report_issue', 'request_instruction', 'provide_details', 'report_completed_step', 'report_failure', 'confirm_resolution', 'request_escalation', 'request_admin_action', 'unknown']
    confidence: float = Field(ge=0, le=1)
    needs_clarification: bool


logger = logging.getLogger('uvicorn.error')


async def refine(rag, classifier, safe, baseline, context):
    usage = {}
    def finish(reason, result=baseline, status=None):
        logger.info('classification reason=%s http_status=%s', reason, status)
        return result.model_copy(update={'generation_usage': usage,
            'generation_reason': reason, 'generation_http_status': status})
    if safe.flags:
        return finish('safety_blocked')
    if not rag.settings.generation_enabled:
        return finish('generation_disabled')
    if not baseline.needs_clarification:
        return finish('classification_already_resolved')
    try:
        raw, usage = await rag.generate_classification({'query': safe.text, 'history': context})
        candidate = Candidate.model_validate(raw)
    except RagError as exc:
        return finish(str(exc), status=exc.status)
    except ValidationError:
        return finish('invalid_generation_response', status=200)
    if candidate.confidence < rag.settings.generation_confidence_threshold:
        return finish('confidence_below_threshold', status=200)
    if candidate.needs_clarification:
        return finish('clarification_required', status=200)
    if candidate.domain == 'out_of_scope':
        if baseline.domain == 'it_support' or candidate.category is not None or candidate.subcategory is not None:
            return finish('domain_conflict', status=200)
        return finish('llm_classification_accepted', Classification(domain='out_of_scope',
            confidence=candidate.confidence, method='llm'), 200)
    if candidate.domain != 'it_support':
        return finish('uncertain_domain', status=200)
    pair = (candidate.category, candidate.subcategory)
    if pair not in classifier.pairs:
        return finish('invalid_taxonomy_pair', status=200)
    if baseline.category and baseline.category != pair[0]:
        return finish('category_conflict', status=200)
    return finish('llm_classification_accepted', Classification(domain='it_support', category=pair[0], subcategory=pair[1],
                          intent='request_admin_action' if pair == ('ACCESS', 'PERMISSIONS') else candidate.intent,
                          priority=classifier.pairs[pair], confidence=candidate.confidence,
                          method='llm', kb_available=pair in classifier.kb), 200)
