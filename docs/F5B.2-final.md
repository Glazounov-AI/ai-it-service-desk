# F5B.2 final correction

D36/D37: share action-specific explicit result recognition between preflight and decision engine. The tested VPN sequence completes without upstream requests in local mode. Local decisions now report strategy=local. No changes to RAG or dependencies.

Regression: 209 passed on Python 3.13.5; Windows Python 3.14.4 and live acceptance pending.

Limitations: conservative phrase rules, not general natural-language understanding. The resource-name rule covers the tested portal/file-server phrase; other names can use the existing `Ресурсы: ...` format. Context limits remain unchanged to avoid unmeasured classification degradation. Real upstream outage and all-mode comparison remain pending. No blanket trust in LLM intent.

## Final integration acceptance

- Regression: 209 Service Desk tests, 108 RAG tests.
- Integration: 60 requests, 59 HTTP 200/201, one HTTP 504.
- Request tracing: 60/60.
- VPN diagnostic workflow: PASS in all four configurations.
- Complete VPN ticket drafts: 4/4.
- Diagnostic tokens: query 6279, retrieve 30, local 0.
- Diagnostic token reduction: 99.52% retrieve, 100% local.
- Total comparable token reduction: 57.30% retrieve.
- Mean initial diagnostic latency: query 19137.5 ms,
  retrieve 3654.5 ms, local 161 ms.
- Offline VPN workflow and initial Outlook diagnostics: PASS.
- Offline classification fallback and metadata: PASS.
- D32, D34, D35, D36, D37: accepted within tested scope.

Decision: GO with limitations.

Remaining limitations:
- One consultation timeout (HTTP 504, 28007 ms).
- Production p95 and load acceptance pending F5C.
- Classifier context reduction deferred.
- Natural-language action recognition remains rule-based.
- Local knowledge base version consistency must be maintained.
- Failed request token usage is unknown.

Recommended MVP diagnostic strategy: local.

