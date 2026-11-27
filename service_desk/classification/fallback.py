"""Neutral fallback when the provider cannot determine the domain."""
def unavailable_domain(classification):
    return classification.domain == 'uncertain' and classification.generation_reason in {
        'generation_timeout', 'generation_connection_error', 'generation_http_error', 'invalid_generation_response'
    }

NEUTRAL_QUESTION = 'Не удалось определить тему запроса. Если вопрос касается корпоративной IT-поддержки, уточните его. Можно также повторить запрос позже.'
