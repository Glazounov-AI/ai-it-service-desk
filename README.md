# AI IT Service Desk

**AI-powered assistant for first-line internal IT support.**

[English](#english) | [Русский](#русский)

---

# English

## Project Overview

AI IT Service Desk is an AI-powered assistant designed to automate common first-line internal IT support requests.

The assistant identifies the type of issue, asks clarifying questions when necessary, retrieves relevant instructions from the Knowledge Base, guides the employee through troubleshooting, and escalates unresolved issues to the appropriate IT team.

The project is designed as a professional prototype of an AI-powered IT Service Desk, with a focus on Knowledge Base-grounded troubleshooting, controlled escalation, security boundaries, and measurable assistant quality.

## Project Goals

- Reduce the workload on first-line IT support.
- Provide faster responses to common employee IT requests.
- Standardize troubleshooting procedures.
- Reduce unsupported or hallucinated technical recommendations.
- Route unresolved requests to the appropriate IT team.
- Prepare structured information for creating a Service Desk ticket.

## Core Workflow

```text
User Request
      ↓
Intent Classification
      ↓
Clarification (if required)
      ↓
Knowledge Base Lookup
      ↓
Troubleshooting
      ↓
Resolution Check
      ↓
 ┌──────────┴──────────┐
 ↓                     ↓
Resolved          Not Resolved
                       ↓
                   Escalation
                       ↓
                  Ticket Draft
```

## Initial Request Taxonomy

| Category | Description |
|---|---|
| `ACCESS` | Accounts, passwords and permissions |
| `MFA` | Multi-factor authentication |
| `EMAIL` | Corporate email |
| `VPN` | Remote access and VPN |
| `SOFTWARE` | Software installation and application issues |
| `HARDWARE` | Workstations and peripheral devices |
| `NETWORK` | Network and connectivity problems |
| `OTHER` | Requests that do not match known categories |

The taxonomy will be extended with subcategories as the Knowledge Base grows.

## Assistant Boundaries

The assistant:

- uses approved Knowledge Base materials as the source for technical procedures;
- does not invent troubleshooting procedures that are absent from the available documentation;
- does not grant permissions or modify user accounts;
- does not perform administrative actions;
- asks clarifying questions when a request is ambiguous;
- does not request unnecessary sensitive information;
- escalates an issue when it cannot be safely resolved using the available Knowledge Base;
- clearly distinguishes troubleshooting instructions from actions that require an IT specialist.

## Current Capabilities

- IT request classification;
- Knowledge Base-grounded troubleshooting;
- clarification of ambiguous requests;
- step-by-step troubleshooting procedures;
- support-group routing;
- escalation when no approved resolution is available;
- security and administrative-action boundaries;
- documented System Prompt;
- completed 20-scenario baseline functional test suite;
- regression testing and documented investigation of observed limitations.

## Planned Enhancements

- hierarchical request classification;
- expanded Knowledge Base coverage;
- more complex multi-step diagnostic scenarios;
- structured ticket draft generation;
- broader regression dataset;
- integration-level testing outside the Playground environment;
- Service Desk API integration.

## Planned Ticket Output

For unresolved requests, the assistant will be able to prepare structured information for a future Service Desk integration.

Example:

```json
{
  "category": "ACCESS",
  "subcategory": "MFA",
  "priority": "normal",
  "assigned_group": "Identity & Access",
  "issue_summary": "MFA unavailable after phone replacement",
  "kb_article": "KB-017",
  "troubleshooting_completed": true,
  "resolution": "not_resolved",
  "action": "escalate"
}
```

The current project does not automatically create tickets or perform administrative actions. Service Desk API integration is considered a future extension.

## Repository Structure

```text
ai-it-service-desk/
├── prompts/
│   └── system-prompt.md
├── knowledge-base/
│   ├── it-knowledge-base.csv
│   ├── it-knowledge-base.md
│   ├── routing-table.csv
│   └── routing-table.md
├── scenarios/
│   ├── test-scenarios.md
│   └── example-dialogues.md
├── docs/
│   ├── project-description.md
│   ├── user-guide.md
│   └── knowledge-base-guide.md
├── tests/
│   └── test-results.md
├── CHANGELOG.md
└── README.md
```

## Development Roadmap

### v0.1 — Project Foundation

Project structure, architecture, initial request taxonomy and documentation framework.

### v0.5 — Working Prototype

Initial Knowledge Base, routing table, System Prompt and core troubleshooting scenarios.

### Current Development — Validated Prototype

Full 20-scenario functional validation, prompt regression testing, documented limitations, and documentation hardening.

### v1.0 — First Stable Release

Stable documented assistant baseline with validated core behavior, expanded regression coverage, consistent project documentation, and portfolio-ready presentation.

### Future Development

Knowledge Base expansion, advanced diagnostic scenarios, structured ticket generation, integration testing, and Service Desk API integration.

## Current Status

**Current development stage: Validated Prototype**

Core assistant components are implemented and the baseline 20-scenario functional test suite has been completed. All scenarios passed functionally. System Prompt 0.2 is the current prompt version.

The project is now focused on documentation hardening, broader regression coverage, Knowledge Base expansion, and preparation for the first stable release.

---

# Русский

## О проекте

AI IT Service Desk — ИИ-ассистент первой линии внутренней IT-поддержки сотрудников компании.

Ассистент определяет тип проблемы, при необходимости задаёт уточняющие вопросы, находит подходящую инструкцию в базе знаний (Knowledge Base), проводит сотрудника через пошаговую диагностику и передаёт нерешённую проблему соответствующей группе IT-поддержки.

Проект разрабатывается как профессиональный прототип AI IT Service Desk с акцентом на диагностику на основе Knowledge Base, контролируемую эскалацию, соблюдение границ безопасности и измеримую оценку качества ассистента.

## Цели проекта

- Снизить нагрузку на первую линию IT-поддержки.
- Ускорить обработку типовых IT-запросов сотрудников.
- Стандартизировать процедуры диагностики.
- Снизить риск неподтверждённых или выдуманных технических рекомендаций.
- Маршрутизировать нерешённые обращения в соответствующую IT-группу.
- Подготавливать структурированную информацию для создания заявки в Service Desk.

## Основной сценарий работы

```text
Запрос сотрудника
        ↓
Классификация запроса
        ↓
Уточнение (при необходимости)
        ↓
Поиск в Knowledge Base
        ↓
Пошаговая диагностика
        ↓
Проверка результата
        ↓
 ┌───────────┴───────────┐
 ↓                       ↓
Решено                Не решено
                          ↓
                      Эскалация
                          ↓
                    Черновик заявки
```

## Начальная классификация запросов

| Категория | Назначение |
|---|---|
| `ACCESS` | Учётные записи, пароли и права доступа |
| `MFA` | Многофакторная аутентификация |
| `EMAIL` | Корпоративная электронная почта |
| `VPN` | Удалённый доступ и VPN |
| `SOFTWARE` | Установка ПО и проблемы приложений |
| `HARDWARE` | Компьютеры и периферийные устройства |
| `NETWORK` | Сеть и проблемы подключения |
| `OTHER` | Запросы, не относящиеся к известным категориям |

По мере развития Knowledge Base категории будут дополнены подкатегориями.

## Ограничения ассистента

Ассистент:

- использует утверждённые материалы Knowledge Base как источник технических процедур;
- не придумывает отсутствующие в документации способы решения;
- не выдаёт права доступа и не изменяет учётные записи;
- не выполняет административные действия;
- задаёт уточняющие вопросы при неоднозначном запросе;
- не запрашивает лишние чувствительные данные;
- эскалирует проблему, если её нельзя безопасно решить с помощью доступной Knowledge Base;
- отделяет инструкции, которые пользователь может выполнить самостоятельно, от действий, требующих IT-специалиста.

## Текущие возможности

- классификация IT-запросов;
- диагностика на основе Knowledge Base;
- уточнение неоднозначных запросов;
- пошаговые процедуры диагностики;
- маршрутизация по группам поддержки;
- эскалация при отсутствии утверждённого решения;
- соблюдение ограничений безопасности и административных действий;
- документированный System Prompt;
- выполненный базовый набор из 20 функциональных тестовых сценариев;
- регрессионное тестирование и документирование выявленных ограничений.

## Планируемое развитие

- иерархическая классификация запросов;
- расширение Knowledge Base;
- более сложные многошаговые диагностические сценарии;
- генерация структурированного черновика заявки;
- расширение набора регрессионных тестов;
- интеграционное тестирование вне среды Playground;
- интеграция с Service Desk API.

## Формирование заявки

Для нерешённых проблем ассистент сможет подготовить структурированные данные для последующей интеграции с Service Desk.

Пример:

```json
{
  "category": "ACCESS",
  "subcategory": "MFA",
  "priority": "normal",
  "assigned_group": "Identity & Access",
  "issue_summary": "MFA unavailable after phone replacement",
  "kb_article": "KB-017",
  "troubleshooting_completed": true,
  "resolution": "not_resolved",
  "action": "escalate"
}
```

В текущей версии проекта ассистент не создаёт реальные заявки и не выполняет административные действия. Интеграция с Service Desk API рассматривается как дальнейшее развитие проекта.

## Структура репозитория

```text
ai-it-service-desk/
├── prompts/
│   └── system-prompt.md
├── knowledge-base/
│   ├── it-knowledge-base.csv
│   ├── it-knowledge-base.md
│   ├── routing-table.csv
│   └── routing-table.md
├── scenarios/
│   ├── test-scenarios.md
│   └── example-dialogues.md
├── docs/
│   ├── project-description.md
│   ├── user-guide.md
│   └── knowledge-base-guide.md
├── tests/
│   └── test-results.md
├── CHANGELOG.md
└── README.md
```

## Этапы разработки

### v0.1 — Project Foundation

Структура проекта, архитектура, начальная классификация запросов и каркас документации.

### v0.5 — Working Prototype

Первая версия Knowledge Base, таблица маршрутизации, System Prompt и основные диагностические сценарии.

### Текущая разработка — Validated Prototype

Полная функциональная проверка по 20 сценариям, регрессионное тестирование промпта, документирование выявленных ограничений и актуализация документации.

### v1.0 — First Stable Release

Стабильная документированная версия ассистента с проверенным базовым поведением, расширенным регрессионным покрытием, согласованной документацией и готовым представлением проекта.

### Дальнейшее развитие

Расширение Knowledge Base, сложные диагностические сценарии, генерация структурированных заявок, интеграционное тестирование и интеграция с Service Desk API.

## Текущий статус

**Текущий этап разработки: Validated Prototype**

Основные компоненты ассистента реализованы, базовый набор из 20 функциональных тестовых сценариев полностью выполнен. Все сценарии пройдены функционально. Текущая версия System Prompt — 0.2.

Следующий этап проекта — актуализация документации, расширение регрессионного покрытия и Knowledge Base, а также подготовка первой стабильной версии.
