from contextlib import contextmanager
from .storage import SessionError


class SessionService:
    def __init__(self, repository, rag):
        self.repository = repository
        self.rag = rag
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
            self.repository.append(sid, 'user', query)
            result = await self.rag.query(query)
            self.repository.append(sid, 'assistant', result.answer,
                                   result.model_dump(exclude={'query', 'answer'}))
            return result

    def close(self, sid):
        with self.exclusive(sid):
            return self.repository.transition(sid, 'closed')
