# Defect register — F3.7
D01–03 classifier confidence/context/intent: corrected in tested cases. D04–08 targeted retrieval, context, grounding, diagnostic state and escalation: managed workflow implemented; not general guarantees. D09 premature classification: bounded preflight fixes. D10–13 timeout coordination, startup indexing, external diagnostics and token optimization: F5. D14–17 count routing, context-free followups, inconsistent classification, unnecessary generation: corrected in tested cases. D18 information-collection step may be marked completed by generic failure; draft remains incomplete. D19–23 account/MFA/software/VPN/BIOS and KB reference issues: F37A passed original scenarios. D24 no authentication/ownership: blocker for public deployment, not local F4. D25 ambiguous paraphrases outside rules remain uncertain. Additional limitations: MFA yes/no phases are not separately modeled; generic failure after backup attempt may repeat question. Single-process locking, no retention/pagination, no draft supplementation, no external submission. Safety regex coverage is bounded, not universal secret detection. No claim of production readiness.

## F4 — дополнение

| ID | Статус |
|---|---|
| D26 | Исправлен в проверенной ветке VPN; контекстные правила ограничены |
| D27 | Исправлен в проверенных сценариях типизированных действий; пользователь подтвердил отсутствие цикла |
| D28 | Исправлен, пять автоматических сценариев MFA |
| D29 | Исправлен, два сценария исчерпания действий |
| D30 | Исправлен в проверенных цепочках; критерий TS-022 сохранён |
| D18 | Проверены три сценария сбора ресурсов; полнота произвольных сведений не гарантирована |

F4C-final: 198 тестов в среде Python 3.13.5; локальная регрессия 3.14.4 ожидается.
