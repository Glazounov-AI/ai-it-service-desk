# F5B.2 — configurable diagnostic lookup

Defaults preserve legacy behavior. Set SERVICE_DESK_DIAGNOSTIC_LOOKUP=retrieve and SERVICE_DESK_RAG_API_KEY to the RAG API key for index verification without completion. Set lookup=local to use the existing approved CSV without index verification. SERVICE_DESK_TARGETED_CONSULTATION=true restricts consultation retrieval to the known article for a resolved classification. Unknown classifications retain existing behavior. Neutral fallback metadata matches the response.

Local mode trusts the CSV and does not establish index freshness. Retrieval mode verifies source presence, not equivalence to the CSV. Context reduction is deferred until comparative classification evaluation. No live provider acceptance performed here.
