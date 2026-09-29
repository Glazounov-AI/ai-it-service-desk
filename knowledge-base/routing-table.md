# AI IT Service Desk — Routing Table

**Version:** 0.1  
**Purpose:** Request classification, routing, and escalation rules

---

## 1. Purpose

This document defines how employee IT requests should be classified and routed.

Use it to determine:

- request category and subcategory;
- responsible Support Group;
- whether user-side troubleshooting is normally possible;
- whether administrative action may be required;
- default priority;
- escalation condition.

The Routing Table defines **where an issue belongs**.

The Knowledge Base defines **how the issue should be troubleshot**.

Do not use the Routing Table as a substitute for a Knowledge Base troubleshooting procedure.

---

## 2. Routing Table

| Category | Subcategory | Request Type | Support Group | Self-Resolve | Admin Action | Priority | Escalation Condition |
|---|---|---|---|---|---|---|---|
| `ACCESS` | `PASSWORD` | Change or recover corporate account password | `Identity & Access` | yes | no | normal | KB procedure fails or administrative password reset is required |
| `ACCESS` | `ACCOUNT_LOCKED` | Corporate account is locked | `Identity & Access` | no | yes | normal | Administrative account unlocking is required |
| `ACCESS` | `PERMISSIONS` | Access permission request or issue | `Identity & Access` | no | yes | normal | Permissions must be granted, modified, or revoked |
| `ACCESS` | `LOGIN_FAILED` | Unable to sign in to corporate account | `Identity & Access` | yes | conditional | normal | Standard troubleshooting fails or account change is required |
| `MFA` | `CODE_NOT_RECEIVED` | MFA verification code is not received | `Identity & Access` | yes | conditional | normal | Standard troubleshooting fails or MFA configuration must be changed |
| `MFA` | `PHONE_REPLACED` | Phone or authentication device replaced | `Identity & Access` | conditional | yes | normal | MFA re-registration or administrative MFA change is required |
| `MFA` | `AUTHENTICATOR` | Microsoft Authenticator issue | `Identity & Access` | yes | conditional | normal | Troubleshooting fails or MFA re-registration is required |
| `EMAIL` | `OUTLOOK_START` | Microsoft Outlook does not start | `Service Desk` | yes | no | normal | Application troubleshooting does not resolve the issue |
| `EMAIL` | `SEND_RECEIVE` | Email cannot be sent or received | `Service Desk` | yes | conditional | normal | Issue persists after standard troubleshooting |
| `EMAIL` | `PROFILE` | Microsoft Outlook profile issue | `Service Desk` | conditional | conditional | normal | Profile recreation or specialist intervention is required |
| `EMAIL` | `MAILBOX_ACCESS` | No access to mailbox or shared mailbox | `Identity & Access` | conditional | yes | normal | Mailbox access permissions must be modified |
| `VPN` | `CLIENT_START` | Corporate VPN client does not start | `Service Desk` | yes | no | normal | VPN client troubleshooting does not resolve the issue |
| `VPN` | `AUTHENTICATION` | VPN authentication failure | `Identity & Access` | yes | conditional | normal | Account and MFA checks do not resolve the issue |
| `VPN` | `CONNECTION` | VPN connection cannot be established | `Network` | yes | conditional | normal | Standard connection troubleshooting does not resolve the issue |
| `VPN` | `RESOURCE_ACCESS` | VPN connected but corporate resources unavailable | `Network` | yes | conditional | normal | VPN is connected but corporate resources remain unavailable |
| `SOFTWARE` | `INSTALL_REQUEST` | Software installation request | `Workplace` | conditional | yes | normal | Software is unavailable in approved catalog or installation requires administrative privileges |
| `SOFTWARE` | `APP_START` | Corporate application does not start | `Service Desk` | yes | no | normal | Standard application troubleshooting does not resolve the issue |
| `SOFTWARE` | `APP_ERROR` | Error while using corporate application | `Service Desk` | yes | conditional | normal | Error persists after documented KB procedure |
| `SOFTWARE` | `UPDATE` | Software update problem | `Workplace` | yes | conditional | normal | Approved update procedure cannot complete successfully |
| `HARDWARE` | `PC_START` | Computer does not power on or boot | `Workplace` | conditional | no | high | Basic power and connection checks do not resolve the issue |
| `HARDWARE` | `PERIPHERAL` | Keyboard, mouse, headset, or other peripheral does not work | `Workplace` | yes | no | normal | Reconnection and standard troubleshooting do not resolve the issue |
| `HARDWARE` | `PRINTER` | Printer issue | `Workplace` | yes | conditional | normal | Documented printer troubleshooting does not resolve the issue |
| `HARDWARE` | `DISPLAY` | Monitor or display issue | `Workplace` | yes | no | normal | Connection and display checks do not resolve the issue |
| `NETWORK` | `WIFI` | Cannot connect to corporate Wi-Fi | `Network` | yes | conditional | normal | Standard Wi-Fi troubleshooting does not resolve the issue |
| `NETWORK` | `LAN` | No wired network connection | `Network` | yes | conditional | normal | Cable, connection, and network adapter checks do not resolve the issue |
| `NETWORK` | `INTERNET` | No Internet access | `Network` | yes | conditional | normal | Issue cannot be isolated to workstation or affects multiple users |
| `NETWORK` | `SHARED_RESOURCE` | Shared network resource unavailable | `Network` | yes | conditional | normal | Network works but shared resource remains unavailable |
| `OTHER` | `UNKNOWN` | Request does not match a known category | `Service Desk` | no | conditional | normal | No appropriate category or KB article can be identified |

---

## 3. Field Values

### Self-Resolve

- `yes` — an approved user-side procedure may normally be attempted.
- `no` — the request normally requires IT involvement.
- `conditional` — user-side actions may be possible depending on the situation.

### Admin Action

- `yes` — administrative action is required.
- `no` — administrative action is not normally required.
- `conditional` — administrative action may become necessary depending on the troubleshooting result.

### Priority

Current default priority values:

- `normal`
- `high`

Default priority is a starting value, not a complete impact assessment.

---

## 4. Routing Rules

1. Select the most appropriate `Category` and `Subcategory` using the available information.

2. If several routes are possible, ask a focused clarification question before selecting one.

3. Do not classify a request using only a technical keyword when the full context indicates another issue.

4. After classification, use the corresponding Knowledge Base article when one exists.

5. The Routing Table does not authorize undocumented troubleshooting.

6. If no suitable Knowledge Base article exists, do not invent a procedure.

7. Follow the defined `Escalation Condition` when troubleshooting cannot continue or administrative action is required.

8. Preserve Support Group names exactly as defined:
   - `Service Desk`
   - `Identity & Access`
   - `Network`
   - `Workplace`

9. Do not translate Support Group names in user-facing responses.

10. Use `OTHER / UNKNOWN` only when a more specific classification cannot be reliably determined.

11. Routing identifies the responsible Support Group. It does not mean that a real ticket has been created or transferred.

12. Do not increase priority solely because the user describes the request as urgent.
