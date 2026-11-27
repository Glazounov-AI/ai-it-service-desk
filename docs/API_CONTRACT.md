# API contract for F4
Development API 1.1.0.dev3. JSON UTF-8; local base http://127.0.0.1:9992. Managed diagnostics must be enabled. No authentication or ownership enforcement yet: local UI only.

| Method | Path | Result |
|---|---|---|
| GET | /health | status, service |
| POST | /sessions | {user_id: string 1–128}, 201 SessionResponse |
| GET | /sessions/{id} | SessionResponse |
| POST | /sessions/{id}/messages | {query: string 1–2000}, RagResponse |
| GET | /sessions/{id}/messages | MessageResponse[] |
| GET | /sessions/{id}/diagnostic-case | DiagnosticCase |
| GET / POST | /sessions/{id}/ticket-draft | TicketDraft; POST ensures existing eligible draft |
| POST | /sessions/{id}/close | SessionResponse |
| POST | /consult | Stateless RagResponse, not managed workflow |

SessionResponse: id,user_id,status,created_at,updated_at,closed_at. RagResponse: query,answer,from_cache,model,retrieved_sources,usage,strategy,classification. MessageResponse: id,session_id,role,content,metadata,created_at. DiagnosticCase and TicketDraft schemas are available in /openapi.json. UI must render text safely, not HTML, and never request secrets. Display incomplete drafts as incomplete; no actual ticket submission. Refresh session/case/draft after each turn. Disable concurrent sends; 409 means conflict, 404 missing session or draft, 422 invalid request, 429 rate limit, 502/503/504 upstream error. Managed fallback can return 200 with unavailable message: do not interpret HTTP 200 alone as successful diagnosis. No automatic resend after ambiguous timeout. States new,clarifying,troubleshooting,awaiting_result,resolved,escalation_required,ticket_draft_ready,closed. Disable messages in terminal states. No pagination, authentication or public exposure.
