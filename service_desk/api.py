from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, HTTPException, Request
from .config import Settings
from .models import ConsultationRequest, RagResponse
from .rag_client import RagClient, RagError


def create_app(settings: Settings | None = None, transport=None):
    @asynccontextmanager
    async def lifespan(app):
        config = settings or Settings.from_env()
        async with httpx.AsyncClient(timeout=config.rag_timeout, transport=transport,
                                     follow_redirects=False, trust_env=False) as client:
            app.state.rag = RagClient(client, config)
            yield

    app = FastAPI(title='AI IT Service Desk — development API', version='1.1.0.dev2', lifespan=lifespan)

    @app.get('/health')
    async def health():
        return {'status': 'ok', 'service': 'ai-it-service-desk'}

    @app.post('/consult', response_model=RagResponse)
    async def consult(body: ConsultationRequest, request: Request):
        try:
            return await request.app.state.rag.query(body.query)
        except RagError as exc:
            raise HTTPException(status_code=exc.status, detail=str(exc)) from None

    return app


app = create_app()
