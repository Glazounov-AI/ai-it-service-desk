from typing import Literal
from pydantic import BaseModel, Field


class Classification(BaseModel):
    domain: Literal['it_support', 'out_of_scope', 'uncertain']
    category: str | None = None
    subcategory: str | None = None
    intent: str = 'unknown'
    priority: str | None = None
    confidence: float = Field(ge=0, le=1)
    method: Literal['rules', 'fallback'] = 'rules'
    needs_clarification: bool = False
    clarification_question: str | None = None
    safety_flags: list[str] = Field(default_factory=list)
    kb_available: bool | None = None
