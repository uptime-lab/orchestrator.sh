---
title: How it works
summary: What boots a board, what runs on it, and which step checks which.
section: Start
---
A board boots a small recovery system from your server. An agent inside it writes the operating system and then keeps the board managed. This page follows that path and says what is checked at each step.

## The parts

| Part | Where it runs | What it does |
|---|---|---|
| Server | Your machine, or our hosted service | Web UI and API, the device channel, OS image storage, and the signer that prepares bootloaders |
| Bootloader | The board's EEPROM | Holds the server's name and public key, and fetches the recovery system |
| Recovery image | The board's RAM | A 98 MB Linux system with the agent inside. It does not touch the drive by itself |
| Agent | Recovery, and later the installed OS | Connects out to the server, runs your commands and reports back |



## Network boot without PXE

The board uses the HTTP boot built into the Raspberry Pi bootloader:

1. It gets an ordinary address from the network's DHCP server.
2. Its bootloader asks the server, by name, for the recovery image and its signature over HTTP on port 80.
3. It checks the signature against the key it holds, loads the image into RAM and starts it.

Nothing changes on the router, and the server can be on another network or on the internet. Plain HTTP is enough because the bootloader checks the signature: an image signed by another key does not boot.

The bootloader learns the server's name and key once per board: from the browser over USB, with a provisioning card, or from a board that already runs Linux ([Adding a device](../add-a-device/)).

## From blank to ready

1. You approve the board by its hardware serial.
2. The server prepares a bootloader for that board and the agent writes it.
3. The board boots the recovery system from the server.
4. The agent streams the OS image you picked onto the drive.
5. The agent installs itself into the new system with the board's own credential.
6. The board boots from its drive and reports in.

Over the internet this takes about six minutes on a Compute Module 4 or 5 ([Installing an operating system](../install-an-os/)).

## When the OS is broken

A board whose drive cannot be booted goes round its boot order and asks the server again, about every 30 seconds. Set its **Boot behavior** to **Recovery** and the next request gets the recovery system. No power cycle is needed. In two runs a board with a wiped drive was back in recovery 57 and 73 seconds after the switch.

![plasma-rig-01, whose drive was wiped, is OFFLINE in the Nodes list; opening it, going to Properties and clicking Recovery under Boot behavior starts a timer, and with no reboot command the node turns violet RECOVERY, its hostname changing to the recovery name, 1 minute 13 seconds after the click](img/how-it-works/v1-broken-os-to-recovery.mp4 "A board that cannot boot its drive reaches recovery on its own after the switch; the wait is fast-forwarded")

A board whose system starts and then hangs does not ask again by itself. It needs a reboot: a power cycle, or a watchdog you armed beforehand ([Hardware and the watchdog](../hardware-and-watchdog/)).

## What checks what

| Step | Checked by | How |
|---|---|---|
| Recovery image | Bootloader | RSA signature made with the server's own key, created when you turn network boot on |
| Agent in recovery | Bootloader | The agent is part of the signed image. Recovery downloads no code |
| OS image | Agent | SHA-256 sent with the install command. The agent writes the first part of the image last, so a drive that fails the check never becomes bootable |
| Agent package | Server, then agent | Signature made on hardware keys kept offline. The server checks a release on import, the agent checks the package before installing it |
| Commands and secrets | TLS | The device channel uses TLS whenever the server has an `https` address |

The agent carries the public keys that verify agent packages, so a board installs only agents signed for the build it runs. A fork built from source replaces that key set and signs its own releases ([ARTIFACT-SIGNING.md](https://github.com/uptime-lab/orchestrator/blob/main/docs/ARTIFACT-SIGNING.md)).

## Where the chain stops

- **This is not Secure Boot.** The bootloader's key is stored in the EEPROM, not fused into the board. Someone who holds the board, or has root on it, can write another key.
- **The installed OS boots unsigned.** The signature covers the recovery system. The board boots the image you installed as it is.
- **OS images are not signed.** The checksum is only as trustworthy as the channel that carried it. On a local server over plain HTTP, that channel is not encrypted.
- **The server is trusted.** Whoever controls your server controls your boards.

> **Note:** A local server without a certificate sends commands and secrets unencrypted. Use it on a network you trust, or give the server a DNS name and let the installer get a certificate.

Next: [Adding a device](../add-a-device/).
