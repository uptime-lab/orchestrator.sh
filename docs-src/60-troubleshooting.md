---
title: Troubleshooting
summary: Find what you see, why it happens, and what to do.
section: Administration
---
## A device does not appear

- **A card-booted device shows a login prompt and never appears.** The card has a GUID partition table. In macOS Disk Utility, choose **View** → **Show All Devices**, select the card itself, erase it as **MS-DOS (FAT)** with scheme **Master Boot Record**, and unzip the bundle again.
- **A device another server managed ignores the card and boots its old system.** Its bootloader tries network, NVMe, USB, then SD. Remove the drive while the card does its work, or [flash the board from the browser](../add-a-device/#flash-a-board-from-the-browser).
- **The one command seems to hang on a new system.** The system's first package upgrade holds the package manager, for up to about half an hour on a fresh Ubuntu. The script waits and names the process holding the lock once a minute. Leave it running.
- **The node appears as PENDING.** A device from **One command** or **Master image** waits for approval. Open it, check the **HW serial** and click **Approve**. By default Admins and Super Admins can approve.
- **The backend log says `adoption handshake rejected … node not found`.** The device presents an identity from another server or from a node you deleted. Flash it from the browser. If you adopted it again here, click **Update bootloader** on the new node.

## A node is stuck in recovery or will not boot its system

- **A device that already ran its own OS comes back in recovery.** Its bootloader boots from this server, and its **Boot behavior** is **Inherit**, which means **Recovery** unless you changed the account default. Set it to **Local OS** in **Properties** and reboot.
- **A node boots into nothing, or into a system this server did not install.** It is set to **Local OS**, and its drive holds no system with this server's agent. Set **Boot behavior** to **Recovery** and power-cycle it. Then [install an OS](../install-an-os/) and set **Local OS**.
- **Reboot to recovery is refused.** The node is offline, or its bootloader does not try network boot first. Bring the node online, or click **Update bootloader** in **Advanced** → **Bootloader / EEPROM**.
- **A node goes offline on and off for up to half an hour after an OS install.** The fresh system runs its first package upgrade, which restarts services. Wait. It settles when the upgrade ends.

## A command or install does not finish

- **Install OS shows an image but you can't pick it.** The image has no uploaded file, no checksum yet, or is still being processed. The label says which. Wait, or upload the file in **Operations** → **Install images**.
- **Install OS fails with "device … is mounted".** The node is using that drive. Check the **Target Device** and pick the drive you mean to erase.
- **Install OS fails during the download.** The node tries an interrupted download up to three times by itself. If it still fails, run **Install OS** again.
- **After a failed install the node keeps booting recovery.** It stays there until an install succeeds, so it never boots a half-written disk. Run **Install OS** and **Install Agent** again.
- **A command stays Queued.** The node is offline. Changes of state wait up to a day: access, hostname, watchdog, LEDs, hardware profile, utilities, overclock and agent updates. A queued command that waits longer ends as **Expired**. A reboot, a script, an identify or an OS install fails at once instead.
- **Status shows "Command stopped reporting".** A command the node accepted has said nothing for 30 minutes, usually because its report was lost. It settles when the node reconnects, for example after a power-cycle.
- **Restore of a deleted node is refused.** Its board was adopted again as another node in this account, named in the deleted node's row. Delete that node first.
- **The uninstall script ends with `NOT DONE`.** Another package operation held the package manager, so the agent package is still installed. Run the script again once that operation has finished.

## I cannot sign in

- **You forgot your password or lost your authenticator app.** Use a recovery code if you saved them. Otherwise the operator resets it from the server's command line in one command ([Recover a lost password or authenticator](https://github.com/uptime-lab/orchestrator/blob/main/docs/INSTALL.md#recover-a-lost-password-or-authenticator)).

## The server will not start after an upgrade

- **The page loads but every request fails with 502.** The backend refuses a database that a newer release has already migrated. Run `docker compose -f docker-compose.community.yml logs backend | grep -i schema` in the install directory to see why. Go forward to the newer release again, or restore the backup you took before the upgrade. There is no downgrade.
- **After an upgrade, nothing answers on ports 443, 80 and 50051.** The proxy cannot read its route files under `proxy/`. Run `chmod -R a+rX proxy` in the install directory, with `sudo` if the files aren't yours, then `docker restart orchestrator-proxy`.
- **The browser shows a self-signed certificate.** The proxy could not get its Let's Encrypt certificate. `DOMAIN` must resolve to this server from the internet, and port 80 must be open to it. `docker logs orchestrator-proxy 2>&1 | grep -i acme` names the reason. Fix it, then run `docker restart orchestrator-proxy`. Let's Encrypt pauses a name for an hour after five failures.

## When nothing here matches

1. Open the node and read **Actions** → **Command history**. A failed command says why.
2. Open **Status** → **Attention** ([Status, attention and the audit trail](../status-and-audit/)).
3. On the server, run `docker compose -f docker-compose.community.yml logs backend` in the install directory.
4. Ask in the [repository's issues](https://github.com/uptime-lab/orchestrator/issues). Report a security problem the private way `SECURITY.md` describes, never in an issue.
