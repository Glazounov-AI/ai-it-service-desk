# AI IT Service Desk

**AI-powered assistant for first-line internal IT support.**

[English](#english) | [Русский](#русский)

---

# English

## Project Overview

AI IT Service Desk is an AI-powered assistant designed to automate common first-line internal IT support requests.

The assistant identifies the type of issue, asks clarifying questions when necessary, retrieves relevant instructions from the Knowledge Base, guides the employee through troubleshooting, and escalates unresolved issues to the appropriate IT team.

The project is being developed as part of a Prompt Engineering course and is designed to evolve from a course MVP into a portfolio-ready prototype of an AI-powered IT Service Desk.

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

## Planned Capabilities

### Course MVP — v1.0

- IT request classification;
- Knowledge Base lookup;
- step-by-step troubleshooting;
- clarifying questions;
- routing by issue category;
- escalation rules;
- example dialogues;
- Knowledge Base maintenance instructions;
- documented system prompt.

### Portfolio Edition — v1.1

- hierarchical request classification;
- extended Knowledge Base;
- multi-step diagnostic scenarios;
- structured escalation;
- ticket draft generation;
- difficult and ambiguous test cases;
- evaluation dataset;
- quality metrics.

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

Initial Knowledge Base, routing table, system prompt and core troubleshooting scenarios.

### v1.0 — Course MVP

Complete implementation of the course requirements.

### v1.1 — Portfolio Edition

Extended Knowledge Base, advanced troubleshooting logic, structured escalation, ticket generation and evaluation.

## Current Status

**Current version: v0.5 — Working Prototype**

Core assistant components are implemented. Initial testing is in progress.

---

# Русский

## О проекте

AI IT Service Desk — ИИ-ассистент первой линии внутренней IT-поддержки сотрудников компании.

Ассистент определяет тип проблемы, при необходимости задаёт уточняющие вопросы, находит подходящую инструкцию в базе знаний (Knowledge Base), проводит сотрудника через пошаговую диагностику и передаёт нерешённую проблему соответствующей группе IT-поддержки.

Проект разрабатывается в рамках курса по промпт-инжинирингу и развивается от учебного MVP до портфельного прототипа AI IT Service Desk.

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

## Планируемые возможности

### Course MVP — v1.0

- классификация IT-запросов;
- поиск решения в Knowledge Base;
- пошаговая диагностика;
- уточняющие вопросы;
- маршрутизация по категории проблемы;
- правила эскалации;
- примеры диалогов;
- инструкция по обновлению Knowledge Base;
- документированный системный промпт.

### Portfolio Edition — v1.1

- иерархическая классификация запросов;
- расширенная Knowledge Base;
- многошаговые диагностические сценарии;
- структурированная эскалация;
- генерация черновика заявки;
- сложные и неоднозначные тестовые сценарии;
- evaluation dataset;
- метрики качества.

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

Первая версия Knowledge Base, таблица маршрутизации, системный промпт и основные диагностические сценарии.

### v1.0 — Course MVP

Полная реализация требований учебного технического задания.

### v1.1 — Portfolio Edition

Расширенная Knowledge Base, развитая логика диагностики, структурированная эскалация, генерация заявок и оценка качества.

## Текущий статус

**Текущая версия: v0.5 — Working Prototype**

Основные компоненты ассистента реализованы. Начинается первичное тестирование.
