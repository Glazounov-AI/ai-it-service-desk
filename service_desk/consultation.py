import asyncio
from .models import RagResponse
from .classification.hybrid import refine
from .rag_client import RagError


class ConsultationService:
    def __init__(self, rag, safety, classifier):
        self.rag = rag
        self.safety = safety
        self.classifier = classifier

    def prepare(self, query):
        safe = self.safety.inspect(query)
        classification = self.classifier.classify(safe.text, safe.flags)
        return safe, classification

    async def classify(self, safe, classification, context=()):
        return await refine(self.rag, self.classifier, safe, classification, list(context))

    async def execute(self, safe, classification):
        if safe.flags:
            result = RagResponse(query=safe.text, answer='Не передавайте пароли, коды и токены и не обходите защиту. Опишите проблему без секретных данных.', from_cache=False, model='local-safety')
        elif self.rag.settings.generation_enabled and classification.domain == 'out_of_scope':
            result = RagResponse(query=safe.text, answer='Я помогаю с корпоративной IT-поддержкой. Задайте вопрос по этой теме.', from_cache=False, model='local-out-of-scope')
        elif self.rag.settings.generation_enabled and classification.needs_clarification:
            result = RagResponse(query=safe.text, answer=classification.clarification_question or 'Уточните проблему.', from_cache=False, model='local-clarification')
        else:
            result = await self.rag.query(safe.text)
        data = self.safety.clean(result.model_dump())
        data['classification'] = classification.model_dump()
        return RagResponse.model_validate(data)
