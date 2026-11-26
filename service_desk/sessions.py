from contextlib import contextmanager
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
            self.repository.append(sid, 'user', safe.text, {'classification': classification.model_dump()})
            result = await self.consultation.execute(safe, classification)
            self.repository.append(sid, 'assistant', result.answer,
                                   result.model_dump(exclude={'query', 'answer'}))
            return result

    def close(self, sid):
        with self.exclusive(sid):
            return self.repository.transition(sid, 'closed')
