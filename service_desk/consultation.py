from .models import RagResponse


class ConsultationService:
    def __init__(self, rag, safety, classifier):
        self.rag = rag
        self.safety = safety
        self.classifier = classifier

    def prepare(self, query):
        safe = self.safety.inspect(query)
        classification = self.classifier.classify(safe.text, safe.flags)
        return safe, classification

    async def execute(self, safe, classification):
        if safe.flags:
            result = RagResponse(query=safe.text, answer='Не передавайте пароли, коды и токены и не обходите защиту. Опишите проблему без секретных данных.', from_cache=False, model='local-safety')
        else:
            result = await self.rag.query(safe.text)
        data = self.safety.clean(result.model_dump())
        data['classification'] = classification.model_dump()
        return RagResponse.model_validate(data)
