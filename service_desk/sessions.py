from .clarification import resolve
import asyncio
from .diagnostic_case import observe
from .decision import DecisionEngine
from .diagnostic_preflight import preflight
from contextlib import contextmanager
from .context import build_context
from .rag_client import RagError
from .storage import SessionError


class SessionService:
    def __init__(self, repository, rag, consultation=None):
        self.repository = repository
        self.rag = rag
        self.consultation = consultation
        self.active = set()
        self.engine = DecisionEngine() if rag is not None and rag.settings.managed_diagnostics else None

    @contextmanager
    def exclusive(self, sid):
        if sid in self.active:
            raise SessionError(409, 'Сессия уже обрабатывает запрос')
        self.active.add(sid)
        try:
            yield
        finally:
            self.active.remove(sid)

    async def consult(self, sid, query):
        with self.exclusive(sid):
            if self.consultation is None:
                raise RuntimeError('Consultation service required')
            safe, classification = self.consultation.prepare(query)
            context = build_context(self.repository.recent_messages(sid), self.consultation.safety)
            message_id = self.repository.append(sid, 'user', safe.text, {'classification': classification.model_dump()})
            try:
                async with asyncio.timeout(28):
                    case = self.repository.get_case(sid)
                    local = preflight(safe, classification, case, self.repository.get(sid)["status"]) if self.engine else None
                    if self.engine and local is None:
                        local = resolve(safe, classification, case, self.repository.get(sid)['status'], self.consultation.classifier)
                    classification = local if local is not None else await self.consultation.classify(safe, classification, context)
                    if self.engine:
                        status = self.repository.get(sid)['status']
                        updated, target, result = await self.engine.decide(case, message_id, safe, classification, status, self.rag)
                        result = type(result).model_validate(self.consultation.safety.clean(result.model_dump()))
                        self.repository.finish_diagnostic_turn(updated, status, target, result)
                        return result
                    updated = observe(case, message_id, safe.text, classification)
                    if updated != case:
                        self.repository.save_case(updated)
                    result = await self.consultation.execute(safe, classification)
            except TimeoutError:
                raise RagError(504, 'Превышено общее время ожидания') from None
            self.repository.append(sid, 'assistant', result.answer,
                                   result.model_dump(exclude={'query', 'answer'}))
            return result

    def close(self, sid):
        with self.exclusive(sid):
            return self.repository.transition(sid, 'closed')
