# AI IT Service Desk — Example Dialogues

[English](#english) | [Русский](#русский)

---

# English

## 1. Purpose

This document demonstrates representative interaction patterns of the AI IT Service Desk assistant.

The examples illustrate how the assistant handles common IT requests using the project Knowledge Base, clarification logic, escalation rules, and security boundaries.

These examples are intended to demonstrate assistant behavior. Formal validation results are documented separately in `tests/test-results.md`.

---

## 2. Outlook Does Not Start

**User:**

> Outlook does not start.

**Assistant:**

> Open Task Manager and check whether an Outlook process is still running.
>
> If an Outlook process is running, close it and start Outlook again.
>
> If the problem persists, restart the computer and try to start Outlook again.
>
> If Outlook still does not start, contact the Service Desk for further diagnostics.

### Demonstrated behavior

- recognizes an email/Outlook issue;
- uses the available troubleshooting procedure;
- provides steps in a clear order;
- escalates when the documented procedure is exhausted.

---

## 3. Ambiguous Network Problem

**User:**

> The network is not working.

**Assistant:**

> Are you connected through corporate Wi-Fi or through a network cable (LAN)?

**User:**

> Through a network cable.

**Assistant:**

> Check that the network cable is connected to the computer.
>
> Check the physical cable connection at the workplace network socket.
>
> Disconnect and reconnect the network cable.
>
> Check whether the network connection status changes.
>
> If the LAN connection is still unavailable, contact the Network support group.

### Demonstrated behavior

- recognizes an ambiguous request;
- does not assume the connection type;
- asks a focused clarification;
- selects the appropriate troubleshooting path after clarification.

---

## 4. VPN Connected but Resource Is Unavailable

**User:**

> VPN connects successfully, but I cannot open a corporate resource.

**Assistant:**

> Verify that the VPN status is `Connected`.
>
> Check access to another corporate resource.
>
> Disconnect and reconnect the VPN.
>
> If corporate resources remain unavailable, record which resources cannot be accessed and contact the Network support group.

### Demonstrated behavior

- distinguishes VPN connection problems from resource-access problems;
- uses targeted troubleshooting rather than restarting the entire VPN procedure;
- provides an escalation path when the issue remains unresolved.

---

## 5. MFA After Phone Replacement

**User:**

> I replaced my phone and now MFA does not work.

**Assistant:**

> Restoring MFA after replacing a registered phone requires the authentication method to be updated or re-registered.
>
> This action requires assistance from the Identity & Access support group.
>
> Do not send your password or MFA verification codes to anyone.

### Demonstrated behavior

- identifies a request involving authentication;
- does not request authentication secrets;
- avoids unsupported administrative instructions;
- routes the request to `Identity & Access`.

---

## 6. Administrator Rights Request

**User:**

> Give me administrator rights so I can install an application.

**Assistant:**

> I cannot grant administrator rights or make changes to your account.
>
> Administrator access requires action by an authorized IT specialist.
>
> Please contact the Service Desk and specify which application you need and why it is required.

### Demonstrated behavior

- respects administrative-action boundaries;
- does not claim capabilities the assistant does not have;
- directs the request to an authorized support process;
- requests useful context for escalation.

---

## 7. No Approved Troubleshooting Procedure

**User:**

> My laptop became very slow to boot after a BIOS update. Which BIOS setting should I change?

**Assistant:**

> Do not change BIOS settings without an approved procedure.
>
> The available Knowledge Base does not contain an approved troubleshooting procedure for slow startup after a BIOS update, so recommending a specific BIOS setting would be unsafe.
>
> Please contact the Service Desk and provide the laptop model and approximately how long startup takes.

### Demonstrated behavior

- recognizes that the available Knowledge Base does not cover the issue;
- does not invent technical instructions;
- avoids potentially unsafe changes;
- escalates with useful diagnostic context.

---

## 8. Security Boundary — MFA Code

**User:**

> Support asked me for my MFA code. Can I send it to you first so you can check it?

**Assistant:**

> No. Do not send an MFA verification code to anyone, including me.
>
> Enter the code only in the official authentication window when you initiated the sign-in yourself.
>
> If the request for the code was unexpected, do not approve it and contact the Service Desk.

### Demonstrated behavior

- refuses collection of authentication secrets;
- provides safe handling guidance;
- treats an unexpected MFA request as a security concern.

---

# Русский

## 1. Назначение

Этот документ содержит примеры типовых взаимодействий с ассистентом AI IT Service Desk.

Примеры показывают работу ассистента с распространёнными IT-запросами с использованием Knowledge Base проекта, логики уточнения, правил эскалации и ограничений безопасности.

Примеры предназначены для демонстрации поведения ассистента. Формальные результаты проверки документированы отдельно в `tests/test-results.md`.

---

## 2. Не запускается Outlook

**Пользователь:**

> Не запускается Outlook.

**Ассистент:**

> Откройте Task Manager и проверьте, остался ли запущенный процесс Outlook.
>
> Если процесс Outlook запущен, завершите его и снова запустите Outlook.
>
> Если проблема сохраняется, перезагрузите компьютер и попробуйте снова запустить Outlook.
>
> Если Outlook по-прежнему не запускается, обратитесь в Service Desk для дальнейшей диагностики.

### Что демонстрирует пример

- распознавание проблемы с Outlook;
- использование доступной процедуры диагностики;
- последовательное предоставление действий;
- эскалацию после завершения документированной процедуры.

---

## 3. Неоднозначная проблема с сетью

**Пользователь:**

> Не работает сеть.

**Ассистент:**

> Вы подключены к корпоративной Wi-Fi или через сетевой кабель (LAN)?

**Пользователь:**

> Через сетевой кабель.

**Ассистент:**

> Проверьте подключение сетевого кабеля к компьютеру.
>
> Проверьте физическое подключение кабеля к сетевой розетке на рабочем месте.
>
> Отключите и снова подключите сетевой кабель.
>
> Проверьте, изменился ли статус сетевого подключения.
>
> Если LAN-подключение по-прежнему недоступно, обратитесь в группу `Network`.

### Что демонстрирует пример

- распознавание неоднозначного запроса;
- отсутствие предположения о типе подключения;
- уточнение необходимой информации;
- выбор подходящей процедуры после уточнения.

---

## 4. VPN подключён, но ресурс недоступен

**Пользователь:**

> VPN подключается, но я не могу открыть корпоративный ресурс.

**Ассистент:**

> Убедитесь, что статус VPN — `Connected`.
>
> Проверьте доступ к другому корпоративному ресурсу.
>
> Отключите и снова подключите VPN.
>
> Если корпоративные ресурсы остаются недоступны, зафиксируйте, какие именно ресурсы недоступны, и обратитесь в группу `Network`.

### Что демонстрирует пример

- различие между проблемой VPN-соединения и доступом к ресурсу;
- целевую диагностику вместо повторения всей процедуры подключения;
- эскалацию, если проблема сохраняется.

---

## 5. MFA после замены телефона

**Пользователь:**

> Я сменил телефон, и теперь не работает MFA.

**Ассистент:**

> После замены зарегистрированного телефона метод MFA необходимо обновить или зарегистрировать заново.
>
> Для этого требуется помощь группы `Identity & Access`.
>
> Не сообщайте никому свой пароль или MFA-коды подтверждения.

### Что демонстрирует пример

- определение запроса, связанного с аутентификацией;
- отсутствие запроса секретных данных;
- отказ от неподтверждённых административных инструкций;
- маршрутизацию в `Identity & Access`.

---

## 6. Запрос прав администратора

**Пользователь:**

> Дайте мне права администратора, чтобы я мог установить приложение.

**Ассистент:**

> Я не могу самостоятельно выдать права администратора или изменить вашу учётную запись.
>
> Для предоставления административного доступа требуются действия авторизованного IT-специалиста.
>
> Обратитесь в Service Desk и укажите, какое приложение необходимо установить и для какой задачи оно требуется.

### Что демонстрирует пример

- соблюдение ограничений на административные действия;
- отсутствие заявлений о несуществующих возможностях ассистента;
- передачу запроса авторизованной IT-поддержке;
- сбор полезного контекста для эскалации.

---

## 7. В Knowledge Base нет утверждённой процедуры

**Пользователь:**

> После обновления BIOS ноутбук стал очень медленно загружаться. Какую настройку BIOS изменить?

**Ассистент:**

> Не меняйте настройки BIOS без утверждённой процедуры.
>
> В доступной Knowledge Base нет утверждённой процедуры для медленной загрузки после обновления BIOS, поэтому рекомендовать конкретную настройку было бы небезопасно.
>
> Обратитесь в Service Desk и укажите модель ноутбука и примерно сколько времени занимает загрузка.

### Что демонстрирует пример

- определение отсутствия подходящей процедуры в Knowledge Base;
- отказ от выдуманных технических инструкций;
- предотвращение потенциально небезопасных изменений;
- эскалацию со сбором полезной диагностической информации.

---

## 8. Граница безопасности — MFA-код

**Пользователь:**

> Поддержка попросила мой MFA-код. Можно сначала отправить его вам, чтобы вы проверили?

**Ассистент:**

> Нет. Не отправляйте MFA-код никому, в том числе мне.
>
> Введите его только в официальном окне входа, если вы сами начали вход.
>
> Если запрос был неожиданным, не подтверждайте его и сообщите в Service Desk.

### Что демонстрирует пример

- отказ от получения секретных данных аутентификации;
- безопасные рекомендации по использованию MFA-кода;
- обработку неожиданного запроса MFA как потенциальной проблемы безопасности.
