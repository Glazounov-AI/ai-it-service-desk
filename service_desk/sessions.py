import asyncio
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
            self.repository.append(sid, 'user', safe.text, {'classification': classification.model_dump()})
            try:
                async with asyncio.timeout(28):
                    classification = await self.consultation.classify(safe, classification, context)
                    result = await self.consultation.execute(safe, classification)
            except TimeoutError:
                raise RagError(504, 'Превышено общее время ожидания') from None
            self.repository.append(sid, 'assistant', result.answer,
                                   result.model_dump(exclude={'query', 'answer'}))
            return result

    def close(self, sid):
        with self.exclusive(sid):
            return self.repository.transition(sid, 'closed')
