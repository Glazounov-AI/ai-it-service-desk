# AI IT Service Desk — Knowledge Base

**Version:** 0.2
**Purpose:** Internal IT support Knowledge Base
**Supported environment:** Windows 10, Windows 11, Microsoft 365, corporate network and services

---

## KB-001 — Change Corporate Account Password

**Category:** `ACCESS`
**Subcategory:** `PASSWORD`
**Environment:** Corporate Account
**OS:** `ALL`
**Support Group:** `Identity & Access`

### Symptoms

The user wants to change a known current password.

### User Actions

1. Open the corporate password change page.
2. Sign in using the current credentials.
3. Select the password change option.
4. Enter the current password and the new password.
5. Confirm the change.

### Expected Result

The password is successfully changed and the user can sign in using the new password.

### Escalation Condition

Escalate to `Identity & Access` if the password cannot be changed or the user does not know the current password.

---

## KB-002 — Account Locked

**Category:** `ACCESS`
**Subcategory:** `ACCOUNT_LOCKED`
**Environment:** Corporate Account
**OS:** `ALL`
**Support Group:** `Identity & Access`

### Symptoms

The user receives a message stating that the account is locked.

### User Actions

1. Verify that the correct corporate account is being used.
2. Do not continue repeated login attempts.
3. Prepare the account name and error description for IT support.

### Expected Result

The request is ready for administrative account unlocking.

### Escalation Condition

Escalate to `Identity & Access`. Administrative account unlocking is required.

---

## KB-003 — Corporate Account Login Failure

**Category:** `ACCESS`
**Subcategory:** `LOGIN_FAILED`
**Environment:** Corporate Account
**OS:** `ALL`
**Support Group:** `Identity & Access`

### Symptoms

Login fails because of an incorrect password or another login error without an account-lock message.

### User Actions

1. Check the keyboard layout and Caps Lock.
2. Enter the credentials again.
3. Check whether the same corporate account can sign in to another corporate service.

### Expected Result

The user successfully signs in to the corporate account.

### Escalation Condition

Escalate to `Identity & Access` if the error persists after the basic checks or the account becomes locked.

---

## KB-004 — MFA Code Not Received

**Category:** `MFA`  
**Subcategory:** `CODE_NOT_RECEIVED`  
**Environment:** Microsoft 365 / MFA  
**OS:** `ALL`  
**Support Group:** `Identity & Access`

### Symptoms

The user does not receive a verification code during sign-in.

### User Actions

1. Check the selected verification method.
2. Verify that the registered phone is available.
3. Wait for the current code delivery attempt to complete.
4. Request a new code once.

### Expected Result

The verification code is received and sign-in is successfully confirmed.

### Escalation Condition

Escalate to `Identity & Access` if the code is still not received or the registered device is unavailable.

---

## KB-005 — MFA After Phone Replacement

**Category:** `MFA`  
**Subcategory:** `PHONE_REPLACED`  
**Environment:** Microsoft 365 / MFA  
**OS:** `ALL`  
**Support Group:** `Identity & Access`

### Symptoms

The user replaced the phone and can no longer confirm MFA.

### User Actions

1. Check whether another previously configured verification method is available.
2. If a backup method is available, use it to sign in.
3. Do not remove existing MFA methods without confirmed access to the account.

### Expected Result

The user confirms sign-in using an available backup method.

### Escalation Condition

Escalate to `Identity & Access` if no verification method is available or MFA re-registration is required.

---

## KB-006 — Microsoft Authenticator Issue

**Category:** `MFA`  
**Subcategory:** `AUTHENTICATOR`  
**Environment:** Microsoft Authenticator  
**OS:** `ALL`  
**Support Group:** `Identity & Access`

### Symptoms

The approval request does not appear or cannot be accepted in Microsoft Authenticator.

### User Actions

1. Make sure the phone has Internet access.
2. Open Microsoft Authenticator manually.
3. Verify that the correct corporate account is selected.
4. Request authentication again.

### Expected Result

The authentication request appears and the user can confirm the sign-in.

### Escalation Condition

Escalate to `Identity & Access` if Microsoft Authenticator remains unavailable or re-registration is required.

---

## KB-007 — Outlook Does Not Start

**Category:** `EMAIL`  
**Subcategory:** `OUTLOOK_START`  
**Environment:** Microsoft Outlook  
**OS:** `WIN10|WIN11`  
**Support Group:** `Service Desk`

### Symptoms

Microsoft Outlook does not open or closes immediately after launch.

### User Actions

1. Open Task Manager and check for running Outlook processes.
2. If an Outlook process is still running, close it.
3. Start Outlook again.
4. If the problem persists, restart the computer.
5. Try to start Outlook again.

### Expected Result

Microsoft Outlook starts normally.

### Escalation Condition

Escalate to `Service Desk` if Outlook still does not start after the computer restart.

---

## KB-008 — Outlook Does Not Send or Receive Email

**Category:** `EMAIL`  
**Subcategory:** `SEND_RECEIVE`  
**Environment:** Microsoft Outlook / Microsoft 365  
**OS:** `WIN10|WIN11`  
**Support Group:** `Service Desk`

### Symptoms

Outlook starts, but new messages are not received or messages cannot be sent.

### User Actions

1. Check the Internet connection.
2. Check the Outlook connection status.
3. Check whether email works through the Microsoft 365 web interface.
4. Restart Outlook.

### Expected Result

Email sending and receiving are restored.

### Escalation Condition

Escalate to `Service Desk` if webmail works but Outlook still does not synchronize, or if the problem otherwise persists.

---

## KB-009 — VPN Client Does Not Start

**Category:** `VPN`  
**Subcategory:** `CLIENT_START`  
**Environment:** Corporate VPN Client  
**OS:** `WIN10|WIN11`  
**Support Group:** `Service Desk`

### Symptoms

The corporate VPN client does not open.

### User Actions

1. Check Task Manager for an already running VPN client process.
2. If a stuck VPN client process exists, close it.
3. Start the VPN client again.
4. Restart the computer if the client still does not start.

### Expected Result

The VPN client starts normally.

### Escalation Condition

Escalate to `Service Desk` if the VPN client does not start after the computer restart.

---

## KB-010 — VPN Connection Cannot Be Established

**Category:** `VPN`  
**Subcategory:** `CONNECTION`  
**Environment:** Corporate VPN  
**OS:** `WIN10|WIN11`  
**Support Group:** `Network`

### Symptoms

The VPN client starts, but the VPN connection cannot be established.

### User Actions

1. Check whether normal Internet access works.
2. Disconnect and reconnect the VPN.
3. Record the error message or error code if one is displayed.

### Expected Result

The VPN connection is established.

### Escalation Condition

Escalate to `Network` if Internet access works but the VPN connection still cannot be established.

---

## KB-011 — Corporate Resources Unavailable Through VPN

**Category:** `VPN`  
**Subcategory:** `RESOURCE_ACCESS`  
**Environment:** Corporate VPN  
**OS:** `WIN10|WIN11`  
**Support Group:** `Network`

### Symptoms

The VPN shows an active connection, but internal corporate resources cannot be accessed.

### User Actions

1. Verify that the VPN status is `Connected`.
2. Check access to another corporate resource.
3. Disconnect and reconnect the VPN.
4. Record which corporate resources remain unavailable.

### Expected Result

Corporate resources become accessible through the VPN.

### Escalation Condition

Escalate to `Network` if the VPN is connected but one or more corporate resources remain unavailable.

---

## KB-012 — Software Installation Request

**Category:** `SOFTWARE`  
**Subcategory:** `INSTALL_REQUEST`  
**Environment:** Managed Windows Workstation  
**OS:** `WIN10|WIN11`  
**Support Group:** `Workplace`

### Symptoms

The user needs additional software.

### User Actions

1. Check whether the application is available in the approved corporate software catalog.
2. If it is available, use the standard corporate installation procedure.
3. If it is not available, do not download or install it from an unapproved third-party source.

### Expected Result

The approved application is installed using the standard corporate procedure.

### Escalation Condition

Escalate to `Workplace` if the application is not available in the corporate catalog or installation requires administrative privileges.

---

## KB-013 — Network Printer Does Not Print

**Category:** `HARDWARE`  
**Subcategory:** `PRINTER`  
**Environment:** Network Printer  
**OS:** `WIN10|WIN11`  
**Support Group:** `Workplace`

### Symptoms

A print job is submitted, but the document is not printed.

### User Actions

1. Check whether the printer is powered on.
2. Check the printer display for an obvious error.
3. Verify that the correct printer is selected.
4. Remove the user's own stuck print job from the print queue.
5. Try printing again.

### Expected Result

The document prints successfully.

### Escalation Condition

Escalate to `Workplace` if the printer is unavailable to multiple users or the standard troubleshooting procedure does not resolve the issue.

---

## KB-014 — Cannot Connect to Corporate Wi-Fi

**Category:** `NETWORK`  
**Subcategory:** `WIFI`  
**Environment:** Corporate Wi-Fi  
**OS:** `WIN10|WIN11`  
**Support Group:** `Network`

### Symptoms

The computer cannot connect to the corporate Wi-Fi network.

### User Actions

1. Verify that Wi-Fi is enabled.
2. Check whether the corporate Wi-Fi network is visible.
3. Turn Wi-Fi off and on again.
4. Try connecting to the corporate Wi-Fi network again.

### Expected Result

The connection to the corporate Wi-Fi network is restored.

### Escalation Condition

Escalate to `Network` if the corporate Wi-Fi network is not visible or the connection continues to fail.

---

## KB-015 — LAN Connection Unavailable

**Category:** `NETWORK`  
**Subcategory:** `LAN`  
**Environment:** Corporate LAN  
**OS:** `WIN10|WIN11`  
**Support Group:** `Network`

### Symptoms

The computer has no network connection through Ethernet.

### User Actions

1. Check that the network cable is connected to the computer.
2. Check the physical cable connection at the workplace network socket.
3. Disconnect and reconnect the network cable.
4. Check whether the network connection status changes.

### Expected Result

The LAN connection is restored.

### Escalation Condition

Escalate to `Network` if the physical connection has been checked but the LAN remains unavailable.

---

## KB-016 — Computer Does Not Power On or Boot

**Category:** `HARDWARE`
**Subcategory:** `PC_START`
**Environment:** `Managed Windows Workstation`
**OS Version:** `WIN10|WIN11`
**Support Group:** `Workplace`

### Symptoms

The computer does not power on or does not begin the normal boot process.

### User Actions

1. Check that the computer is connected to power.
2. If an external power adapter or power cable is used, check that it is securely connected to both the computer and the power source.
3. If the computer is connected through a power strip or docking station, check that the device providing power is switched on and connected.
4. Disconnect and reconnect the external power connection.
5. Attempt to power on the computer again.
6. Record any visible error message or unusual indicator shown during the startup attempt.

### Expected Result

The computer powers on and begins the normal boot process.

### Escalation Condition

The computer still does not power on or begin the normal boot process after the external power and connection checks.

Do not open the computer case, change BIOS settings, or attempt hardware repair.

Escalate the request to `Workplace`.

---

# Knowledge Base Rules

1. These articles contain the approved troubleshooting procedures for the current project version.
2. Do not infer undocumented corporate procedures from article titles or symptoms.
3. Do not invent internal URLs, server names, credentials, configuration values, or administrative procedures.
4. If no article matches the user's issue, follow the escalation rules defined by the System Prompt.
5. `ALL` means the article is not dependent on the Windows version.
6. `WIN10|WIN11` means the article applies to both Windows 10 and Windows 11.
7. Support Group names must be preserved in their defined English form.
