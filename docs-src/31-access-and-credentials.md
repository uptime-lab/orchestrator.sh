---
title: Access: SSH keys and device users
summary: Add your SSH keys and create the Linux users your nodes should have.
section: Operating a fleet
---
On **Credentials** you add SSH keys and create the Linux users the agent maintains on your nodes. Where a user applies follows the unit rules on [Organizational units and policies](../organization/).

## Add an SSH key

1. Open **Credentials** and the **SSH Keys** tab.
2. Click **Add SSH key**.
3. Under **Paste public key**, type an **Alias**.
4. Paste one public key line, such as `ssh-ed25519 …`.
5. Click **Create Key**.

![The Add SSH Key panel with Alias "Field tablet" and an ssh-ed25519 public key pasted](img/access-and-credentials/02-add-ssh-key.jpg)

Paste one key per entry. A value with several lines saves, but the device refuses it. A key grants nothing until you attach it to a user.

**Generate keypair** creates a key the platform uses to adopt devices over the network. You don't log in with it.

## Create a user on a unit

1. Open the **Users** tab.
2. Select the unit in the left rail, or **All nodes** for the whole account.
3. Click **Add user**.
4. Type the **Username**.
5. Tick or clear **Grant sudo**.
6. Pick your key under **SSH keys** and click **Attach**.
7. Click **Create user**.

![The Add user panel for Garage with username fieldtech, Grant sudo ticked and the key Field tablet attached](img/access-and-credentials/05-add-user.jpg)

A sudo user with no password gets `sudo` without a prompt on every node in its scope. Set a **Password** if you want one. The device only ever receives a salted hash of it.

Click a user to change it. Changes in that panel save at once.

## What happens on the devices

The account appears on online nodes right away and on offline nodes when they reconnect. A node in the recovery system gets it once it is back on its installed OS.

Deleting a user locks the account on its nodes and keeps the home directory. The same happens when a user loses its last key and has no password. Accounts you created by hand on a node are never touched.

To check one node, open it and go to **Properties → Credentials**. **Scan** lists the real accounts on its disk, marked **managed** or **unmanaged**.

![The Credentials section of a node: users from All nodes and from its unit, and On the device listing ubuntu as unmanaged and technician and auditor as managed](img/access-and-credentials/07-node-access.jpg)

> **Warning:** Before you set **Password login** to **Refused (keys only)**, log in to one of the unit's nodes with your key. If the key doesn't work, those nodes become unreachable over SSH.

If you do lock yourself out, add a key or a password to a user in that scope. The change reaches the node over the agent's own connection.

## Trust a CA for certificate logins

Add your certificate authority's public key on **CA Certificates** and drag it onto a unit or **All nodes**. A node then accepts a certificate signed by that CA when it names one of a user's **Certificate principals**.

Next: [Secrets and variables](../secrets-and-variables/).
