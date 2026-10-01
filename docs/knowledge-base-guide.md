# AI IT Service Desk — Knowledge Base Guide

[English](#english) | [Русский](#русский)

---

# English

## 1. Purpose

This document describes how the AI IT Service Desk Knowledge Base is structured and maintained.

The Knowledge Base is the primary source of approved troubleshooting procedures used by the assistant. Technical troubleshooting instructions should be grounded in the available Knowledge Base rather than generated from assumptions or general technical knowledge.

The guide is intended for project maintainers and contributors who add, review, or update Knowledge Base content.

---

## 2. Knowledge Base Files

The project stores Knowledge Base data in two representations:

```text
knowledge-base/
+-- it-knowledge-base.csv
+-- it-knowledge-base.md
+-- routing-table.csv
L-- routing-table.md
```

### `it-knowledge-base.csv`

Structured representation of troubleshooting articles.

It is intended for machine-readable processing, filtering, testing, and future integrations.

### `it-knowledge-base.md`

Human-readable representation of the Knowledge Base.

It is intended for review, documentation, and use in environments where Markdown files are supplied directly as assistant context.

### `routing-table.csv`

Structured mapping between request categories, subcategories, and support groups.

### `routing-table.md`

Human-readable representation of the routing rules.

The CSV and Markdown versions should describe the same logical data.

---

## 3. Current Knowledge Base Coverage

The current Knowledge Base contains 16 troubleshooting articles.

The covered areas include:

- account access;
- password issues;
- account lockout and login failures;
- MFA;
- Outlook;
- email send/receive issues;
- VPN;
- corporate software requests;
- network printers;
- corporate Wi-Fi;
- LAN connectivity.

Current request categories include:

```text
ACCESS
MFA
EMAIL
VPN
SOFTWARE
HARDWARE
NETWORK
OTHER
```

Knowledge Base coverage is intentionally limited at the current project stage.

The absence of an article must not be treated as permission for the assistant to invent a troubleshooting procedure.

---

## 4. Article Identification

Each Knowledge Base article has a unique identifier.

The current format is:

```text
KB-NNN
```

Examples:

```text
KB-001
KB-002
KB-015
```

New articles should receive a new identifier. Existing identifiers should not be reused for different issues.

Stable identifiers make test scenarios, documentation, and future integrations easier to maintain.

---

## 5. Categories and Subcategories

Each article should belong to a defined request category and, where applicable, a subcategory.

Examples:

```text
ACCESS / PASSWORD
ACCESS / ACCOUNT_LOCKED
ACCESS / LOGIN_FAILED

MFA / CODE_NOT_RECEIVED
MFA / PHONE_REPLACED
MFA / AUTHENTICATOR

EMAIL / OUTLOOK_START
EMAIL / SEND_RECEIVE

VPN / CLIENT_START
VPN / CONNECTION
VPN / RESOURCE_ACCESS

SOFTWARE / INSTALL_REQUEST

HARDWARE / PRINTER

NETWORK / WIFI
NETWORK / LAN
```

Existing category and subcategory names should be reused whenever they accurately describe the new article.

New categories or subcategories should be introduced deliberately and reflected in the routing documentation where necessary.

---

## 6. Troubleshooting Content

A Knowledge Base article should describe an approved troubleshooting procedure for a specific issue.

A useful article should provide enough information for the assistant to:

1. recognize when the procedure applies;
2. provide safe troubleshooting steps;
3. determine whether the issue has been resolved;
4. identify when escalation is required.

Troubleshooting steps should be:

- specific;
- ordered logically;
- safe for an end user to perform;
- limited to actions that do not require unauthorized administrative access;
- written without assuming information that the user has not provided.

If a procedure differs depending on the operating system or environment, the article should make that distinction explicit.

---

## 7. Security Requirements

Knowledge Base procedures must not instruct users to:

- disclose passwords;
- disclose MFA verification codes;
- bypass authentication or security controls;
- disable corporate security mechanisms without an approved procedure;
- obtain or use unauthorized administrative privileges.

Procedures requiring administrative access should clearly indicate that the request must be handled by an authorized IT specialist or support group.

Security restrictions take precedence over troubleshooting convenience.

---

## 8. Escalation

Each troubleshooting procedure should make clear when further troubleshooting should stop and the request should be escalated.

Typical escalation conditions include:

- the documented procedure was completed but the issue remains;
- required permissions are unavailable to the user;
- the requested action requires administrative intervention;
- the Knowledge Base does not contain a safe next step;
- the issue falls outside the documented scope.

The assistant should not extend a procedure with invented technical steps after the documented troubleshooting path has been exhausted.

---

## 9. Routing Table

The routing table maps supported request types to appropriate IT support groups.

Current support groups include:

```text
Service Desk
Identity & Access
Network
Workplace
```

Routing information should remain consistent with Knowledge Base categories and escalation rules.

A routing entry does not automatically mean that a complete troubleshooting article exists for that request type.

Therefore, routing coverage and Knowledge Base coverage should be reviewed separately.

---

## 10. Adding a Knowledge Base Article

When adding an article:

1. Check whether an existing article already covers the issue.
2. Assign a new unique `KB-NNN` identifier.
3. Select the appropriate category and subcategory.
4. Define when the procedure applies.
5. Add only approved and reproducible troubleshooting steps.
6. Define the expected result.
7. Define escalation conditions.
8. Review the procedure for security risks.
9. Update both Knowledge Base representations where applicable.
10. Add or update test scenarios if the new article changes assistant behavior.

A new article should not be considered complete until its behavior can be verified with at least one representative scenario.

---

## 11. Updating an Existing Article

When changing an existing article:

- preserve its identifier unless the article represents a fundamentally different issue;
- verify that the CSV and Markdown representations remain synchronized;
- check whether related routing rules need to change;
- identify existing test scenarios affected by the change;
- rerun relevant regression scenarios;
- document significant behavioral changes in the project history.

Changes to Knowledge Base content may affect assistant behavior even when the System Prompt itself is unchanged.

---

## 12. CSV and Markdown Synchronization

The structured and human-readable Knowledge Base representations should contain equivalent operational information.

After changing Knowledge Base content, verify:

```text
CSV
    ¦
Markdown
    ¦
Routing
    ¦
Tests
```

A change in one representation should not silently leave another representation outdated.

When inconsistencies are found, they should be resolved before treating the Knowledge Base update as complete.

---

## 13. Testing Knowledge Base Changes

Knowledge Base changes should be tested against representative user requests.

Testing should verify:

- correct request classification;
- correct article selection;
- appropriate clarification when information is missing;
- accurate use of documented troubleshooting steps;
- correct escalation behavior;
- compliance with security restrictions;
- absence of unsupported troubleshooting instructions.

Existing regression scenarios should be rerun when a Knowledge Base change could affect previously validated behavior.

---

## 14. Current Limitations

The current Knowledge Base is a prototype dataset and does not represent complete enterprise IT support coverage.

Some request types may exist in the routing structure without a corresponding troubleshooting article.

The current project does not provide an automated synchronization mechanism between CSV and Markdown files.

Knowledge Base updates therefore require deliberate review of the related files and affected test scenarios.

---

# Русский

## 1. Назначение

Этот документ описывает структуру и правила сопровождения Knowledge Base проекта AI IT Service Desk.

Knowledge Base является основным источником утверждённых процедур диагностики, используемых ассистентом. Технические инструкции должны основываться на доступной Knowledge Base, а не формироваться на основе предположений или общих технических знаний модели.

Руководство предназначено для участников проекта, которые добавляют, проверяют или обновляют содержимое Knowledge Base.

---

## 2. Файлы Knowledge Base

В проекте используются два представления Knowledge Base:

```text
knowledge-base/
+-- it-knowledge-base.csv
+-- it-knowledge-base.md
+-- routing-table.csv
L-- routing-table.md
```

### `it-knowledge-base.csv`

Структурированное представление статей диагностики.

Предназначено для машинной обработки, фильтрации, тестирования и будущих интеграций.

### `it-knowledge-base.md`

Человекочитаемое представление Knowledge Base.

Предназначено для проверки, документирования и использования в средах, где Markdown-файлы передаются непосредственно в контекст ассистента.

### `routing-table.csv`

Структурированное соответствие категорий, подкатегорий и групп поддержки.

### `routing-table.md`

Человекочитаемое представление правил маршрутизации.

CSV- и Markdown-версии должны описывать одни и те же логические данные.

---

## 3. Текущее покрытие Knowledge Base

Текущая Knowledge Base содержит 16 статей диагностики.

Она охватывает:

- доступ к учётным записям;
- проблемы с паролями;
- блокировку учётных записей и ошибки входа;
- MFA;
- Outlook;
- проблемы отправки и получения электронной почты;
- VPN;
- запросы на корпоративное ПО;
- сетевые принтеры;
- корпоративный Wi-Fi;
- LAN-подключение.

Текущие категории запросов:

```text
ACCESS
MFA
EMAIL
VPN
SOFTWARE
HARDWARE
NETWORK
OTHER
```

На текущем этапе проекта покрытие Knowledge Base намеренно ограничено.

Отсутствие статьи не означает, что ассистент может самостоятельно придумать процедуру диагностики.

---

## 4. Идентификаторы статей

Каждая статья Knowledge Base должна иметь уникальный идентификатор.

Текущий формат:

```text
KB-NNN
```

Например:

```text
KB-001
KB-002
KB-015
```

Новые статьи должны получать новые идентификаторы. Существующие идентификаторы не следует повторно использовать для других проблем.

Стабильные идентификаторы упрощают сопровождение тестовых сценариев, документации и будущих интеграций.

---

## 5. Категории и подкатегории

Каждая статья относится к определённой категории запроса и, при необходимости, подкатегории.

Примеры:

```text
ACCESS / PASSWORD
ACCESS / ACCOUNT_LOCKED
ACCESS / LOGIN_FAILED

MFA / CODE_NOT_RECEIVED
MFA / PHONE_REPLACED
MFA / AUTHENTICATOR

EMAIL / OUTLOOK_START
EMAIL / SEND_RECEIVE

VPN / CLIENT_START
VPN / CONNECTION
VPN / RESOURCE_ACCESS

SOFTWARE / INSTALL_REQUEST

HARDWARE / PRINTER

NETWORK / WIFI
NETWORK / LAN
```

Существующие категории и подкатегории следует использовать повторно, если они точно соответствуют новой статье.

Новые категории и подкатегории следует вводить осознанно и при необходимости отражать в документации маршрутизации.

---

## 6. Содержание процедуры диагностики

Статья Knowledge Base должна описывать утверждённую процедуру диагностики конкретной проблемы.

Статья должна содержать достаточно информации, чтобы ассистент мог:

1. определить, когда применяется процедура;
2. предложить безопасные шаги диагностики;
3. определить, решена ли проблема;
4. определить момент необходимой эскалации.

Шаги диагностики должны быть:

- конкретными;
- расположенными в логичном порядке;
- безопасными для выполнения конечным пользователем;
- ограниченными действиями, не требующими несанкционированных административных прав;
- сформулированными без предположений о данных, которые пользователь не сообщил.

Если процедура зависит от версии операционной системы или среды, это различие должно быть явно указано в статье.

---

## 7. Требования безопасности

Процедуры Knowledge Base не должны предлагать пользователю:

- сообщать пароль;
- сообщать MFA-код подтверждения;
- обходить механизмы аутентификации или безопасности;
- отключать корпоративные механизмы защиты без утверждённой процедуры;
- получать или использовать несанкционированные административные права.

Если процедура требует административного доступа, должно быть явно указано, что запрос необходимо передать авторизованному IT-специалисту или соответствующей группе поддержки.

Требования безопасности имеют приоритет над удобством диагностики.

---

## 8. Эскалация

В каждой процедуре должно быть понятно, когда дальнейшую диагностику следует прекратить и передать запрос IT-поддержке.

Типовые условия эскалации:

- документированная процедура выполнена, но проблема сохранилась;
- у пользователя отсутствуют необходимые права;
- требуемое действие требует административного вмешательства;
- Knowledge Base не содержит безопасного следующего шага;
- проблема находится вне документированного покрытия.

После завершения документированной процедуры ассистент не должен продолжать диагностику с использованием придуманных технических действий.

---

## 9. Таблица маршрутизации

Routing table связывает типы запросов с соответствующими группами IT-поддержки.

Текущие группы:

```text
Service Desk
Identity & Access
Network
Workplace
```

Маршрутизация должна оставаться согласованной с категориями Knowledge Base и правилами эскалации.

Наличие записи в routing table не означает автоматически, что для этого типа запроса существует полноценная статья диагностики.

Поэтому покрытие маршрутизации и покрытие Knowledge Base следует проверять отдельно.

---

## 10. Добавление статьи Knowledge Base

При добавлении статьи:

1. Проверьте, не покрывается ли проблема существующей статьёй.
2. Назначьте новый уникальный идентификатор `KB-NNN`.
3. Выберите соответствующие категорию и подкатегорию.
4. Определите условия применения процедуры.
5. Добавьте только утверждённые и воспроизводимые шаги диагностики.
6. Определите ожидаемый результат.
7. Определите условия эскалации.
8. Проверьте процедуру на риски безопасности.
9. При необходимости обновите оба представления Knowledge Base.
10. Добавьте или обновите тестовые сценарии, если новая статья изменяет поведение ассистента.

Новая статья не должна считаться полностью готовой, пока её поведение нельзя проверить хотя бы одним репрезентативным сценарием.

---

## 11. Обновление существующей статьи

При изменении существующей статьи:

- сохраняйте её идентификатор, если статья не стала описывать принципиально другую проблему;
- проверяйте синхронизацию CSV- и Markdown-представлений;
- проверяйте необходимость изменения связанных правил маршрутизации;
- определяйте существующие тестовые сценарии, затронутые изменением;
- повторно выполняйте соответствующие регрессионные сценарии;
- документируйте существенные изменения поведения в истории проекта.

Изменение Knowledge Base может повлиять на поведение ассистента даже без изменения System Prompt.

---

## 12. Синхронизация CSV и Markdown

Структурированное и человекочитаемое представления Knowledge Base должны содержать эквивалентную рабочую информацию.

После изменения Knowledge Base необходимо проверить:

```text
CSV
    ¦
Markdown
    ¦
Routing
    ¦
Tests
```

Изменение одного представления не должно незаметно оставлять другое представление устаревшим.

Обнаруженные расхождения следует устранить до завершения обновления Knowledge Base.

---

## 13. Тестирование изменений Knowledge Base

Изменения Knowledge Base следует проверять на репрезентативных пользовательских запросах.

Необходимо проверить:

- правильность классификации запроса;
- выбор правильной статьи;
- корректность уточнения при недостатке информации;
- точное использование документированных шагов диагностики;
- правильность эскалации;
- соблюдение ограничений безопасности;
- отсутствие неподтверждённых инструкций.

Если изменение Knowledge Base может повлиять на ранее проверенное поведение, следует повторно выполнить соответствующие регрессионные сценарии.

---

## 14. Текущие ограничения

Текущая Knowledge Base является набором данных прототипа и не представляет полное покрытие корпоративной IT-поддержки.

Некоторые типы запросов могут присутствовать в структуре маршрутизации без соответствующей статьи диагностики.

В текущем проекте нет автоматического механизма синхронизации CSV- и Markdown-файлов.

Поэтому обновление Knowledge Base требует явной проверки связанных файлов и затронутых тестовых сценариев.
