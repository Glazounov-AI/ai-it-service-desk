from pydantic import BaseModel, Field, field_validator


class ConsultationRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)

    @field_validator('query', mode='before')
    @classmethod
    def strip_query(cls, value):
        return value.strip() if isinstance(value, str) else value


class RagResponse(BaseModel):
    query: str
    answer: str = Field(min_length=1)
    from_cache: bool
    model: str
    retrieved_sources: list[dict] = Field(default_factory=list)
    usage: dict = Field(default_factory=dict)
    strategy: str = 'semantic'
