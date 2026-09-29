# AI IT Service Desk — Project Description

[English](#english) | [Русский](#русский)

---

# English

## 1. Project Overview

**AI IT Service Desk** is an AI-powered assistant for first-line internal IT support.

The assistant helps employees resolve common technical issues using an approved Knowledge Base. It identifies the request category, asks clarifying questions when required, selects the relevant troubleshooting procedure, guides the user through the steps, checks the result, and escalates unresolved issues to the appropriate IT support group.

The project is developed as part of a Prompt Engineering course and is designed to evolve from a course MVP into a portfolio-ready prototype.

---

## 2. Business Context

The project models an organization with approximately **150 employees**.

Employees use company-managed computers and standard corporate IT services. A significant part of internal IT support workload consists of repetitive requests that can be resolved using documented procedures.

Typical requests include:

- password and account issues;
- MFA problems;
- corporate email issues;
- VPN connection problems;
- network connectivity;
- software installation and application issues;
- workstation and peripheral problems;
- access and permissions questions.

The purpose of the assistant is to automate the initial handling of these requests without giving the AI administrative access to corporate systems.

---

## 3. Target Users

### Primary users

Company employees who need help with common IT problems.

Users are not expected to have advanced technical knowledge.

### Secondary users

IT support specialists who receive escalated requests.

The assistant should provide them with a structured summary of the issue and troubleshooting steps already completed.

---

## 4. Simulated IT Environment

The project uses a fictional but realistic corporate IT environment.

### Workstations

Supported operating systems:

- Windows 10;
- Windows 11.

Some troubleshooting procedures may differ depending on the Windows version.

If the correct procedure depends on the operating system version and the user has not specified it, the assistant should ask which version is being used before providing version-specific instructions.

### Corporate Services

The simulated environment includes:

- Microsoft 365;
- Microsoft Outlook;
- Microsoft Teams;
- corporate VPN;
- multi-factor authentication (MFA);
- corporate LAN;
- corporate Wi-Fi;
- network printers;
- shared network resources;
- centrally managed corporate software.

The environment may be expanded as the Knowledge Base grows.

---

## 5. IT Support Structure

The simulated IT department contains several support groups.

### Service Desk

First-line support responsible for:

- common user issues;
- basic troubleshooting;
- general IT questions;
- initial request classification;
- request escalation.

### Identity & Access

Responsible for:

- accounts;
- passwords;
- MFA;
- permissions;
- access-related incidents.

### Network

Responsible for:

- LAN;
- Wi-Fi;
- VPN infrastructure;
- network connectivity;
- network-related incidents.

### Workplace

Responsible for:

- Windows workstations;
- laptops and desktops;
- peripheral devices;
- printers;
- standard corporate software;
- workplace configuration.

The routing model may be extended later if additional support areas are required.

---

## 6. Initial Request Taxonomy

The assistant uses the following top-level request categories:

| Category | Description |
|---|---|
| `ACCESS` | Accounts, passwords and permissions |
| `MFA` | Multi-factor authentication |
| `EMAIL` | Corporate email |
| `VPN` | Remote access and VPN |
| `SOFTWARE` | Software installation and application issues |
| `HARDWARE` | Computers and peripheral devices |
| `NETWORK` | LAN, Wi-Fi and connectivity |
| `OTHER` | Requests that do not match known categories |

Subcategories will be introduced as the Knowledge Base develops.

Example:

```text
ACCESS
+-- PASSWORD
+-- ACCOUNT_LOCKED
L-- PERMISSIONS

MFA
+-- CODE_NOT_RECEIVED
+-- PHONE_REPLACED
L-- AUTHENTICATOR
```

---

## 7. Core Workflow

The expected assistant workflow is:

```text
Employee Request
        v
Request Classification
        v
Is the information sufficient?
   v Yes             v No
KB Lookup       Clarifying Question
   v                  v
   L--------------> KB Lookup
                      v
               Troubleshooting
                      v
               Resolution Check
                      v
          ------------+-----------¬
          v                       v
       Resolved                Not Resolved
                                  v
                              Escalation
                                  v
                             Ticket Draft
```

The assistant should not assume that the first interpretation of a request is always correct.

When important information is missing, it should ask a targeted clarifying question before selecting a troubleshooting procedure.

---

## 8. Knowledge Base

The Knowledge Base is the primary source for troubleshooting procedures.

Each Knowledge Base article should contain structured information such as:

- article ID;
- category;
- subcategory;
- issue or symptom;
- applicable environment;
- troubleshooting steps;
- expected result;
- escalation conditions;
- responsible support group.

The assistant must not invent technical procedures that are not supported by the available Knowledge Base.

If no appropriate procedure exists, the issue should be escalated.

---

## 9. Assistant Boundaries

The assistant provides guidance but does not receive administrative privileges.

It must not:

- reset passwords directly;
- unlock accounts;
- grant or revoke permissions;
- create or delete user accounts;
- disable security controls;
- modify MFA configuration on behalf of the user;
- install software directly;
- change corporate infrastructure;
- execute administrative commands on corporate systems;
- claim that an administrative action has been completed when it has not.

When such an action is required, the assistant should explain the next appropriate step and route the request to the responsible IT group.

---

## 10. Clarification Logic

The assistant should request additional information when it materially affects the troubleshooting procedure.

Examples include:

### Operating system

If an instruction differs between Windows 10 and Windows 11:

> Which version of Windows are you using: Windows 10 or Windows 11?

### VPN

If the user only says:

> VPN doesn't work.

The assistant may need to determine whether:

- the VPN client does not start;
- authentication fails;
- the connection is established but corporate resources are unavailable;
- an error message is displayed.

### Email

If the user says:

> Outlook isn't working.

The assistant should determine the relevant symptom before selecting a procedure.

The purpose of clarification is to obtain only information necessary to select the correct troubleshooting path.

---

## 11. Escalation

An issue should be escalated when:

- the Knowledge Base does not contain an appropriate procedure;
- documented troubleshooting has been completed without resolving the issue;
- administrative privileges are required;
- the requested action is outside the assistant's permitted scope;
- the available information indicates that specialist intervention is required.

The assistant should avoid sending the employee back through troubleshooting steps that have already been confirmed as completed.

---

## 12. Ticket Draft

For unresolved requests, the Portfolio Edition will generate a structured ticket draft.

Example:

```json
{
  "category": "MFA",
  "subcategory": "PHONE_REPLACED",
  "priority": "normal",
  "assigned_group": "Identity & Access",
  "issue_summary": "MFA unavailable after phone replacement",
  "kb_article": "KB-017",
  "troubleshooting_completed": true,
  "resolution": "not_resolved",
  "action": "escalate"
}
```

The project does not currently create tickets in an external Service Desk system.

The structured output is designed as an extension point for future API or workflow automation.

---

## 13. Project Scope

### Course MVP — v1.0

The Course MVP will include:

- system prompt;
- request classification;
- Knowledge Base;
- routing table;
- troubleshooting procedures;
- clarification logic;
- escalation rules;
- example dialogues;
- test scenarios;
- Knowledge Base maintenance documentation.

### Portfolio Edition — v1.1

The Portfolio Edition will extend the MVP with:

- hierarchical request taxonomy;
- larger Knowledge Base;
- more complex multi-step troubleshooting;
- structured ticket generation;
- difficult and ambiguous test scenarios;
- evaluation dataset;
- quality metrics;
- documented integration architecture.

---

## 14. Out of Scope

The current project does not include:

- direct access to Active Directory or other identity systems;
- real password resets;
- remote control of employee computers;
- automatic software installation;
- automatic infrastructure changes;
- production Service Desk integration;
- monitoring of corporate devices;
- processing of real employee credentials or other sensitive production data.

These capabilities may be represented conceptually but are not implemented in the current project.

---

# Русский

## 1. Описание проекта

**AI IT Service Desk** — ИИ-ассистент первой линии внутренней IT-поддержки.

Ассистент помогает сотрудникам решать типовые технические проблемы с использованием утверждённой базы знаний (Knowledge Base). Он определяет категорию запроса, при необходимости задаёт уточняющие вопросы, выбирает подходящую инструкцию, проводит пользователя через этапы диагностики, проверяет результат и передаёт нерешённую проблему соответствующей группе IT-поддержки.

Проект разрабатывается в рамках курса по промпт-инжинирингу и развивается от учебного MVP до портфельного прототипа.

---

## 2. Бизнес-контекст

В проекте моделируется организация примерно на **150 сотрудников**.

Сотрудники используют управляемые компанией компьютеры и стандартные корпоративные IT-сервисы. Значительную часть нагрузки внутренней IT-поддержки составляют повторяющиеся обращения, для которых существуют стандартные инструкции.

Типичные обращения:

- проблемы с паролями и учётными записями;
- проблемы с MFA;
- корпоративная электронная почта;
- подключение к VPN;
- проблемы с сетью;
- установка и работа программного обеспечения;
- проблемы с компьютерами и периферией;
- вопросы прав и доступа.

Задача ассистента — автоматизировать первичную обработку таких обращений, не предоставляя ИИ административного доступа к корпоративным системам.

---

## 3. Пользователи

### Основные пользователи

Сотрудники компании, которым требуется помощь с типовыми IT-проблемами.

От пользователя не требуется высокий уровень технической подготовки.

### Вторичные пользователи

Специалисты IT-поддержки, которым передаются нерешённые обращения.

Ассистент должен подготовить для специалиста структурированное описание проблемы и указать уже выполненные шаги диагностики.

---

## 4. Моделируемая IT-инфраструктура

В проекте используется вымышленная, но приближенная к реальной корпоративная IT-среда.

### Рабочие станции

Поддерживаемые операционные системы:

- Windows 10;
- Windows 11.

Некоторые процедуры диагностики могут отличаться в зависимости от версии Windows.

Если инструкция зависит от версии операционной системы, а пользователь её не указал, ассистент должен сначала уточнить, используется Windows 10 или Windows 11, и только после этого выдавать специфичную для версии инструкцию.

### Корпоративные сервисы

Моделируемая инфраструктура включает:

- Microsoft 365;
- Microsoft Outlook;
- Microsoft Teams;
- корпоративный VPN;
- многофакторную аутентификацию (MFA);
- корпоративную LAN;
- корпоративную Wi-Fi-сеть;
- сетевые принтеры;
- общие сетевые ресурсы;
- централизованно управляемое корпоративное ПО.

По мере расширения Knowledge Base инфраструктура может дополняться.

---

## 5. Структура IT-поддержки

В модели используются несколько групп поддержки.

### Service Desk

Первая линия поддержки:

- типовые пользовательские проблемы;
- базовая диагностика;
- общие IT-вопросы;
- первичная классификация обращения;
- передача сложных обращений профильным специалистам.

### Identity & Access

Отвечает за:

- учётные записи;
- пароли;
- MFA;
- права;
- проблемы доступа.

### Network

Отвечает за:

- LAN;
- Wi-Fi;
- VPN-инфраструктуру;
- сетевые подключения;
- сетевые инциденты.

### Workplace

Отвечает за:

- рабочие станции Windows;
- настольные компьютеры и ноутбуки;
- периферийные устройства;
- принтеры;
- стандартное корпоративное ПО;
- настройку рабочего места.

При необходимости модель маршрутизации может быть расширена дополнительными группами.

---

## 6. Начальная классификация запросов

Используются следующие категории верхнего уровня:

| Категория | Назначение |
|---|---|
| `ACCESS` | Учётные записи, пароли и права |
| `MFA` | Многофакторная аутентификация |
| `EMAIL` | Корпоративная электронная почта |
| `VPN` | Удалённый доступ и VPN |
| `SOFTWARE` | Установка ПО и проблемы приложений |
| `HARDWARE` | Компьютеры и периферия |
| `NETWORK` | LAN, Wi-Fi и сетевые подключения |
| `OTHER` | Запросы, не относящиеся к известным категориям |

По мере разработки Knowledge Base будут добавляться подкатегории.

Например:

```text
ACCESS
+-- PASSWORD
+-- ACCOUNT_LOCKED
L-- PERMISSIONS

MFA
+-- CODE_NOT_RECEIVED
+-- PHONE_REPLACED
L-- AUTHENTICATOR
```

---

## 7. Основной сценарий работы

```text
Запрос сотрудника
        v
Классификация
        v
Достаточно ли информации?
   v Да              v Нет
Поиск в KB      Уточняющий вопрос
   v                  v
   L--------------> Поиск в KB
                      v
                  Диагностика
                      v
               Проверка результата
                      v
          ------------+-----------¬
          v                       v
        Решено                 Не решено
                                  v
                              Эскалация
                                  v
                           Черновик заявки
```

Ассистент не должен считать первую интерпретацию запроса автоматически правильной.

Если для выбора инструкции не хватает существенной информации, сначала задаётся целевой уточняющий вопрос.

---

## 8. Knowledge Base

Knowledge Base является основным источником процедур диагностики.

Каждая статья должна содержать структурированную информацию, например:

- ID статьи;
- категорию;
- подкатегорию;
- проблему или симптом;
- применимую среду;
- шаги диагностики;
- ожидаемый результат;
- условия эскалации;
- ответственную группу поддержки.

Ассистент не должен придумывать технические процедуры, отсутствующие в доступной Knowledge Base.

Если подходящей процедуры нет, обращение передаётся специалисту.

---

## 9. Границы возможностей ассистента

Ассистент предоставляет инструкции, но не получает административных полномочий.

Он не должен:

- самостоятельно сбрасывать пароли;
- разблокировать учётные записи;
- выдавать или отзывать права;
- создавать или удалять учётные записи;
- отключать механизмы безопасности;
- самостоятельно изменять настройки MFA пользователя;
- самостоятельно устанавливать программное обеспечение;
- изменять корпоративную инфраструктуру;
- выполнять административные команды в корпоративных системах;
- сообщать пользователю, что административное действие выполнено, если оно фактически не выполнялось.

Если требуется такое действие, ассистент объясняет дальнейший порядок и направляет запрос соответствующей группе IT-поддержки.

---

## 10. Логика уточняющих вопросов

Ассистент запрашивает дополнительную информацию только тогда, когда она влияет на выбор дальнейшей процедуры.

### Версия Windows

Если инструкция различается для Windows 10 и Windows 11:

> Какая версия Windows используется: Windows 10 или Windows 11?

### VPN

Если пользователь сообщает только:

> Не работает VPN.

Ассистенту может потребоваться определить:

- запускается ли VPN-клиент;
- проходит ли аутентификация;
- устанавливается ли соединение;
- доступны ли корпоративные ресурсы после подключения;
- появляется ли сообщение об ошибке.

### Электронная почта

Если пользователь пишет:

> Не работает Outlook.

Ассистент сначала определяет конкретный симптом и только затем выбирает инструкцию.

Цель уточнений — получить минимально необходимую информацию для выбора правильного пути диагностики.

---

## 11. Эскалация

Обращение должно быть передано специалисту, если:

- в Knowledge Base нет подходящей процедуры;
- документированные шаги выполнены, но проблема не решена;
- требуются административные права;
- запрашиваемое действие находится за пределами полномочий ассистента;
- имеющаяся информация указывает на необходимость вмешательства специалиста.

Ассистент не должен заставлять сотрудника повторно выполнять уже подтверждённые шаги диагностики.

---

## 12. Черновик заявки

Для нерешённых обращений Portfolio Edition будет формировать структурированный черновик заявки.

Пример:

```json
{
  "category": "MFA",
  "subcategory": "PHONE_REPLACED",
  "priority": "normal",
  "assigned_group": "Identity & Access",
  "issue_summary": "MFA unavailable after phone replacement",
  "kb_article": "KB-017",
  "troubleshooting_completed": true,
  "resolution": "not_resolved",
  "action": "escalate"
}
```

На текущем этапе проект не создаёт реальную заявку во внешней Service Desk-системе.

Структурированный результат проектируется как точка для будущей интеграции через API или систему автоматизации.

---

## 13. Объём проекта

### Course MVP — v1.0

Учебная версия включает:

- системный промпт;
- классификацию запросов;
- Knowledge Base;
- таблицу маршрутизации;
- процедуры диагностики;
- логику уточняющих вопросов;
- правила эскалации;
- примеры диалогов;
- тестовые сценарии;
- инструкцию по сопровождению Knowledge Base.

### Portfolio Edition — v1.1

Портфельная версия дополнительно включает:

- иерархическую классификацию;
- расширенную Knowledge Base;
- более сложные многошаговые сценарии диагностики;
- структурированную генерацию заявок;
- сложные и неоднозначные тестовые сценарии;
- evaluation dataset;
- метрики качества;
- описание архитектуры будущей интеграции.

---

## 14. За пределами текущего проекта

На данном этапе проект не включает:

- прямой доступ к Active Directory или другим системам управления идентификацией;
- реальный сброс паролей;
- удалённое управление компьютерами сотрудников;
- автоматическую установку ПО;
- автоматическое изменение инфраструктуры;
- production-интеграцию с Service Desk;
- мониторинг корпоративных устройств;
- обработку реальных паролей, учётных данных или других чувствительных production-данных.

Эти возможности могут быть описаны на уровне архитектуры, но не реализуются в текущей версии.
