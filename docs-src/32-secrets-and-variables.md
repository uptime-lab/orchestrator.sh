---
title: Secrets and variables
summary: Store values once and use them on your nodes and in playbooks.
section: Operating a fleet
---
On **Secrets** you store a value once, attach it where it is needed and use it as `{{secrets.NAME}}`. Only account admins and super admins see this page.

A variable stays readable and editable, so use it for URLs, time zones and settings. A secret can't be read back by anyone after you save it, so use it for passwords and keys. Where an attached value reaches follows the unit rules on [Organizational units and policies](../organization/).

## Add a variable or a secret

1. Open **Secrets** and click **Create secret**.
2. Type a **Name**. It is the name you use in `{{secrets.NAME}}`.
3. Choose the **Kind**. **Env** writes the value to the device as an environment variable. **Credential** and **Opaque** are used only by playbooks.
4. Tick **Non-sensitive variable** for a variable, or leave it clear for a secret.
5. Fill in the ENV name, username or label, and the **Value**.
6. Click **Create Secret**.

![Clicking Create secret, typing the name SITE_LABEL, ticking Non-sensitive variable with Kind Env, typing the value garage-east, then closing the panel without saving](img/secrets-and-variables/v1-add-variable.mp4 "Fill in a variable")

**Convert to secret** turns a variable into a secret and can't be undone.

## Attach it to a unit, a node or a tag

A new entry goes nowhere until you attach it. Pick one way:

- Drag its row onto a unit in the left rail.
- On a node, open **Properties → Secrets** and search for it.
- Give it a tag on the **Tags** tab, then attach the tag to a unit or node. Everything carrying the tag goes there, including entries you tag later.

When two entries with the same name reach one node, the nearer level wins. Within one level, a direct attachment beats a tag.

The node's **Secrets** view shows what it receives and from where.

![The Secrets view of a node: API_TOKEN attached directly, and WIFI_PASSWORD, TIMEZONE and REGISTRY_PASSWORD inherited from its unit](img/secrets-and-variables/06-node-secrets.jpg)

**Env** entries land in `/etc/orchestrator/env`, which only root can read. Load them in a systemd service with `EnvironmentFile=/etc/orchestrator/env`. Agents older than 0.8.5 write them to `/etc/environment`, where every login session can read them, so update those agents before you attach secrets.

## Use a value in a playbook

Write `{{secrets.NAME}}` in any text parameter of a [playbook](../playbooks/) step. The server fills it in when the step runs, from the entries that reach that node.

[Utility](../utilities/) parameters accept variables only. A secret is refused there.

> **Warning:** A changed value reaches a device's env file only when the node's access is provisioned again, which happens at an OS install. Playbooks use the new value from their next run. Keep an old credential valid until every node has the new one.

## Manage tokens for new devices

The **Tokens** tab holds master tokens, which new devices present to join your account. One is created for you when you generate a one-command install or download the master image bundle, and **Create token** makes one by hand.

A token is a secret. Anyone holding it, or an SD card built with it, can join devices to your account until it expires, so **Deactivate** tokens you no longer need.

Next: [Utilities: managed software](../utilities/).
