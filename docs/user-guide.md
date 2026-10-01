# AI IT Service Desk — User Guide

[English](#english) | [Русский](#русский)

---

# English

## 1. Purpose

AI IT Service Desk is an AI-powered assistant for first-line internal IT support.

It helps employees resolve common technical issues using approved Knowledge Base procedures. The assistant can identify the type of request, ask clarifying questions, provide troubleshooting instructions, and determine when an issue should be escalated to an IT support team.

The assistant provides guidance only. It does not perform administrative actions or make changes to corporate systems.

---

## 2. What the Assistant Can Help With

The current Knowledge Base covers common requests in the following areas:

- account access and login issues;
- password-related issues;
- MFA;
- Outlook and corporate email;
- VPN;
- corporate software requests;
- network printers;
- corporate Wi-Fi;
- LAN connectivity.

The assistant can also recognize requests that are outside the available Knowledge Base and route them for further support instead of inventing a solution.

---

## 3. How to Ask for Help

Describe the problem in your own words.

Examples:

- `Outlook does not start.`
- `I cannot connect to the VPN.`
- `The network printer is not working.`
- `I replaced my phone and MFA no longer works.`
- `I cannot access the network through a LAN cable.`

You do not need to know the correct IT category or Knowledge Base article.

When possible, include useful context such as:

- the affected application or service;
- what you were trying to do;
- the visible error message or error code;
- whether the issue affects only you or multiple users;
- whether the problem started after a specific change.

Do not send passwords or MFA verification codes.

---

## 4. Clarifying Questions

If the request is ambiguous, the assistant may ask a focused clarification before providing troubleshooting steps.

For example:

**User:**
`The network is not working.`

**Assistant:**
`Are you connected through corporate Wi-Fi or through a network cable (LAN)?`

This prevents the assistant from selecting an incorrect troubleshooting procedure based on assumptions.

---

## 5. Troubleshooting Process

For supported requests, the assistant follows this general process:

```text
User Request
    v
Request Classification
    v
Clarification (if required)
    v
Knowledge Base Lookup
    v
Troubleshooting
    v
Result Check
    v
Resolved / Escalation
```

Troubleshooting instructions are based on the available Knowledge Base.

If the Knowledge Base does not contain an approved procedure for the reported issue, the assistant should not invent additional technical steps.

---

## 6. Escalation

An issue may be escalated when:

- the available Knowledge Base procedure does not resolve the problem;
- no applicable Knowledge Base procedure exists;
- the request requires administrative permissions;
- the requested action must be performed by an IT specialist;
- continuing troubleshooting without an approved procedure would be unsafe.

Depending on the request, the issue may be routed to an appropriate support group such as:

- `Service Desk`
- `Identity & Access`
- `Network`
- `Workplace`

The assistant provides routing guidance but does not create or modify a real Service Desk ticket in the current version.

---

## 7. Security and Privacy

Never send the assistant:

- your password;
- an MFA verification code;
- authentication secrets;
- other credentials.

The assistant should never ask you to disclose a password or MFA code.

If a request involves a protected administrative action, the assistant should direct the request to the appropriate IT support process instead of attempting to bypass security controls.

---

## 8. What the Assistant Cannot Do

The current assistant cannot:

- reset passwords directly;
- unlock accounts directly;
- grant administrator permissions;
- modify user accounts;
- change corporate infrastructure;
- install software on a workstation;
- perform actions in external IT systems;
- create real Service Desk tickets;
- execute administrative commands on behalf of the user.

It can explain approved procedures and identify when an IT specialist is required.

---

## 9. Example Requests

Examples of suitable requests:

- `Outlook does not start.`
- `I cannot send or receive email.`
- `The VPN client does not start.`
- `VPN connects, but I cannot access a corporate resource.`
- `My account is locked.`
- `I replaced my phone and need to restore MFA access.`
- `The office printer is unavailable.`
- `Corporate Wi-Fi is not working.`
- `The LAN connection is not working.`
- `I need a corporate application installed.`

Requests may be written in natural language. Exact Knowledge Base terminology is not required.

---

## 10. Current Limitations

The assistant is currently at v1.0.0 — First Stable Release.

Its technical guidance is limited to procedures available in the project Knowledge Base.

Knowledge Base coverage is intentionally limited and does not represent every possible corporate IT issue.

The assistant does not currently integrate with a production Service Desk, identity-management platform, endpoint-management system, or other administrative infrastructure.

For escalated requests, the assistant can prepare a structured ticket draft, but it does not create a real ticket in an external Service Desk system. External Service Desk integration is planned for future development.

---

# Русский

## 1. Назначение

AI IT Service Desk — ИИ-ассистент первой линии внутренней IT-поддержки.

Он помогает сотрудникам решать типовые технические проблемы с использованием утверждённых процедур из Knowledge Base. Ассистент может определить тип обращения, задать уточняющие вопросы, предоставить инструкции по диагностике и определить, когда проблему необходимо передать группе IT-поддержки.

Ассистент предоставляет рекомендации, но не выполняет административные действия и не вносит изменения в корпоративные системы.

---

## 2. С какими запросами помогает ассистент

Текущая Knowledge Base охватывает типовые обращения по следующим направлениям:

- доступ к учётным записям и проблемы со входом;
- проблемы с паролями;
- MFA;
- Outlook и корпоративная электронная почта;
- VPN;
- запросы на корпоративное ПО;
- сетевые принтеры;
- корпоративный Wi-Fi;
- подключение по LAN.

Ассистент также умеет определять запросы, для которых в доступной Knowledge Base нет подходящей процедуры, и направлять их на дальнейшую поддержку вместо того, чтобы придумывать решение.

---

## 3. Как описать проблему

Опишите проблему своими словами.

Например:

- `Не запускается Outlook.`
- `Не могу подключиться к VPN.`
- `Не работает сетевой принтер.`
- `Сменил телефон, и теперь не работает MFA.`
- `Не работает сеть через LAN-кабель.`

Вам не нужно самостоятельно определять IT-категорию или искать статью Knowledge Base.

По возможности укажите:

- с каким приложением или сервисом возникла проблема;
- что вы пытались сделать;
- текст или код отображаемой ошибки;
- проблема возникла только у вас или у нескольких сотрудников;
- появилась ли проблема после какого-либо изменения.

Не отправляйте пароль или MFA-код.

---

## 4. Уточняющие вопросы

Если запрос неоднозначен, ассистент может сначала задать уточняющий вопрос и только после этого предложить диагностику.

Например:

**Пользователь:**
`Не работает сеть.`

**Ассистент:**
`Вы подключены к корпоративной Wi-Fi или через сетевой кабель (LAN)?`

Это позволяет не выбирать процедуру диагностики на основании предположений.

---

## 5. Процесс диагностики

Для поддерживаемых запросов используется следующий общий процесс:

```text
Запрос пользователя
    v
Классификация запроса
    v
Уточнение (при необходимости)
    v
Поиск в Knowledge Base
    v
Диагностика
    v
Проверка результата
    v
Решено / Эскалация
```

Технические инструкции основываются на доступной Knowledge Base.

Если в Knowledge Base отсутствует утверждённая процедура для конкретной проблемы, ассистент не должен придумывать дополнительные технические действия.

---

## 6. Эскалация

Проблема может быть передана IT-поддержке, если:

- процедура из Knowledge Base не решила проблему;
- подходящая процедура отсутствует;
- запрос требует административных прав;
- действие должен выполнить IT-специалист;
- продолжение диагностики без утверждённой процедуры может быть небезопасным.

В зависимости от обращения может быть определена соответствующая группа поддержки:

- `Service Desk`
- `Identity & Access`
- `Network`
- `Workplace`

Ассистент определяет направление эскалации, но в текущей версии не создаёт и не изменяет реальные заявки в Service Desk.

---

## 7. Безопасность и конфиденциальность

Никогда не отправляйте ассистенту:

- пароль;
- MFA-код подтверждения;
- секреты аутентификации;
- другие учётные данные.

Ассистент не должен запрашивать у пользователя пароль или MFA-код.

Если запрос требует защищённого административного действия, ассистент должен направить пользователя к соответствующему процессу IT-поддержки, а не пытаться обойти механизмы безопасности.

---

## 8. Что ассистент не может делать

В текущей версии ассистент не может:

- самостоятельно сбрасывать пароли;
- самостоятельно разблокировать учётные записи;
- выдавать права администратора;
- изменять учётные записи пользователей;
- изменять корпоративную инфраструктуру;
- устанавливать ПО на компьютер пользователя;
- выполнять действия во внешних IT-системах;
- создавать реальные заявки в Service Desk;
- выполнять административные команды от имени пользователя.

Ассистент может объяснять утверждённые процедуры и определять ситуации, когда требуется IT-специалист.

---

## 9. Примеры запросов

Примеры подходящих запросов:

- `Не запускается Outlook.`
- `Не могу отправлять или получать почту.`
- `Не запускается VPN-клиент.`
- `VPN подключается, но корпоративный ресурс недоступен.`
- `Учётная запись заблокирована.`
- `Сменил телефон и нужно восстановить доступ к MFA.`
- `Не работает офисный принтер.`
- `Не работает корпоративный Wi-Fi.`
- `Не работает подключение по LAN.`
- `Мне нужно установить корпоративное приложение.`

Запрос можно формулировать обычным языком. Знать точные термины Knowledge Base не требуется.

---

## 10. Текущие ограничения

Текущий релиз ассистента — v1.0.0 — First Stable Release.

Технические рекомендации ограничены процедурами, доступными в Knowledge Base проекта.

Текущее покрытие Knowledge Base намеренно ограничено и не охватывает все возможные проблемы корпоративной IT-инфраструктуры.

Ассистент пока не интегрирован с реальной системой Service Desk, системой управления учётными записями, средствами управления рабочими станциями или другой административной инфраструктурой.

Для эскалируемых обращений ассистент может сформировать структурированный черновик заявки, но не создаёт реальную заявку во внешней системе Service Desk. Интеграция с внешней системой Service Desk запланирована как дальнейшее развитие проекта.
