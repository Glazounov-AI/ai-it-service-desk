import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .safety import SafetyFilter
from .classification.classifier import Classifier
from .consultation import ConsultationService
from .storage import SQLiteRepository, SessionError
from .sessions import SessionService
from .config import Settings
from .models import ConsultationRequest, RagResponse, SessionCreate, SessionResponse, MessageResponse
from .rag_client import RagClient, RagError


def create_app(settings: Settings | None = None, transport=None):
    @asynccontextmanager
    async def lifespan(app):
        config = settings or Settings.from_env()
        if config.generation_enabled and not config.generation_key.get_secret_value():
            raise ValueError("Generation key required")
        async with httpx.AsyncClient(timeout=config.rag_timeout, transport=transport,
                                     follow_redirects=False, trust_env=False) as client:
            app.state.rag = RagClient(client, config)
            app.state.consultation = ConsultationService(app.state.rag, SafetyFilter(), Classifier())
            app.state.sessions = SessionService(SQLiteRepository(config.db_path), app.state.rag, app.state.consultation)
            yield

    app = FastAPI(title='AI IT Service Desk — development API', version='1.1.0.dev3', lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return JSONResponse(status_code=422, content={'detail': 'Invalid request'})

    @app.get('/health')
    async def health():
        return {'status': 'ok', 'service': 'ai-it-service-desk'}

    @app.post('/consult', response_model=RagResponse)
    async def consult(body: ConsultationRequest, request: Request):
        try:
            service = request.app.state.consultation
            async with asyncio.timeout(28):
                safe, classification = service.prepare(body.query)
                classification = await service.classify(safe, classification)
                return await service.execute(safe, classification)
        except TimeoutError:
            raise HTTPException(status_code=504, detail="Превышено общее время ожидания") from None
        except RagError as exc:
            raise HTTPException(status_code=exc.status, detail=str(exc)) from None

    @app.exception_handler(SessionError)
    async def session_error(request, exc):
        return JSONResponse(status_code=exc.status, content={'detail': str(exc)})

    @app.post('/sessions', response_model=SessionResponse, status_code=201)
    async def create_session(body: SessionCreate, request: Request):
        if request.app.state.consultation.safety.inspect(body.user_id).flags:
            raise HTTPException(status_code=422, detail='Invalid user identifier')
        return request.app.state.sessions.repository.create(body.user_id)

    @app.get('/sessions/{session_id}', response_model=SessionResponse)
    async def get_session(session_id: str, request: Request):
        return request.app.state.sessions.repository.get(session_id)

    @app.get('/sessions/{session_id}/messages', response_model=list[MessageResponse])
    async def messages(session_id: str, request: Request):
        return request.app.state.sessions.repository.messages(session_id)

    @app.post('/sessions/{session_id}/messages', response_model=RagResponse)
    async def send_message(session_id: str, body: ConsultationRequest, request: Request):
        try:
            return await request.app.state.sessions.consult(session_id, body.query)
        except RagError as exc:
            raise HTTPException(status_code=exc.status, detail=str(exc)) from None

    @app.post('/sessions/{session_id}/close', response_model=SessionResponse)
    async def close_session(session_id: str, request: Request):
        return request.app.state.sessions.close(session_id)

    return app


app = create_app()
