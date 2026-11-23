---
title: Backup, restore and upgrading the server
summary: What to back up, where the restore and upgrade procedures are, and how to update agents.
section: Administration
---
The commands for a self-hosted server are in the reference: [BACKUP-RESTORE.md](https://github.com/uptime-lab/orchestrator/blob/main/docs/BACKUP-RESTORE.md) and [INSTALL.md → Upgrading](https://github.com/uptime-lab/orchestrator/blob/main/docs/INSTALL.md#upgrading).

## What to back up

Paths are as in the community compose file.

- The credential files in `secrets/`.
- The bootloader signing key, `data/eeprom-keys/privkey.pem`.
- The database, as a nightly encrypted dump ([A scripted nightly dump](https://github.com/uptime-lab/orchestrator/blob/main/docs/BACKUP-RESTORE.md#a-scripted-nightly-dump)), copied off the host.
- The key that encrypts your dumps, kept anywhere but the server.
- The `.env` file beside the compose file.
- OS images and agent releases in `data/backend/storage/` or your bucket.
- With the `proxy-tls` proxy, its certificate store `data/proxy/acme.json`. A local-network install has no certificate, and `data/proxy/` stays empty.

> **Warning:** Without `secrets/secrets_encryption_key` the dump restores but nothing encrypted in it can be read. Without `data/eeprom-keys/privkey.pem` no server can sign a boot image your network-booting devices accept, so put both in an escrow you control before you adopt the first device.

## Restore

The reference has two procedures, [into the same install](https://github.com/uptime-lab/orchestrator/blob/main/docs/BACKUP-RESTORE.md#restore-into-the-same-install) and [onto an empty host](https://github.com/uptime-lab/orchestrator/blob/main/docs/BACKUP-RESTORE.md#restore-onto-an-empty-host), and the order of steps matters in both. Prepare an empty host by hand with the same release and `DOMAIN`, because the installer would create new keys and a new owner. Devices reconnect on their own when the restored server keeps the same name and keys.

## Upgrade the server

The full procedure is [INSTALL.md → Upgrading](https://github.com/uptime-lab/orchestrator/blob/main/docs/INSTALL.md#upgrading).

1. Read `CHANGELOG.md` for every release between yours and the new one.
2. Run the dump by hand and check your copies of `secrets/` and `.env`.
3. Get the new release's files, run `chmod -R a+rX proxy` in the install directory, and create any new credential file its compose file names.
4. Set `PLATFORM_VERSION` in `.env` to the new release.
5. Run `docker compose -f docker-compose.community.yml pull`, then `up -d`, and check that every container is up.

There is no downgrade across a schema change, so rolling back means restoring the dump from step 2.

## Update agents on devices

The server hands devices the agent release you marked latest when you imported it (`--set-latest`). To update one node, open it and click **Update** in the **Agent** row on **Overview**, which works only while the node is online.

![The Overview tab of an offline node, welding-bot, with Hostname, Unit, IP, MAC, HW serial, Bootloader and an Agent row showing 0.8.5 and a greyed-out Update button](img/backup-and-upgrade/01-agent-row.jpg "Update is greyed out while the node is offline")

To update many, open **Status** → **Attention**, filter by **Agent update available**, select the rows and click **Update agent**. A node offline at the time gets the update when it reconnects, and a node still finishing another command is held back until it is done.
