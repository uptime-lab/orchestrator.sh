---
title: How it works
summary: What boots a board, what runs on it, and which step checks which.
section: Start
---
A board boots a small recovery system from your server, an agent inside it writes the operating system, and the same agent then keeps the board managed. This page follows that path and says what is checked at each step.

## The parts

| Part | Where it runs | What it does |
|---|---|---|
| Server | Your machine, or our hosted service | Web UI and API, the device channel, storage for OS images, and the signer that prepares bootloaders |
| Bootloader | The board's EEPROM | Holds the server's name and the public half of its signing key, and fetches the recovery system |
| Recovery image | The board's RAM | A 98 MB Linux system with the agent inside. It never touches the drive by itself |
| Agent | Recovery, and later the installed OS | Connects out to the server, runs the commands you send and reports back |

A managed board connects out to the server. The server does not have to reach the board, so boards can sit behind NAT.

## Network boot without PXE

Classic network boot needs a DHCP server that hands out boot options and a TFTP server on the same network. Uptime Orchestrator uses the HTTP boot built into the Raspberry Pi bootloader instead:

1. The board gets an ordinary address from whatever DHCP server the network has.
2. Its bootloader asks the server, by name, for the recovery image and its signature over HTTP on port 80.
3. It checks the signature against the key it holds, loads the image into RAM and starts it.

Nothing changes on the router, and the server can be on another network or on the internet. The connection is plain HTTP because the bootloader checks the signature itself: an image signed by another key does not boot.

The bootloader learns the server's name and key once per board. You do it from the browser over USB, with a provisioning card, or from a board that already runs Linux ([Adding a device](../add-a-device/)).

## From blank to managed

1. You approve the board by its hardware serial.
2. The server prepares a bootloader for that board and the agent writes it.
3. The board boots the recovery system from the server.
4. The agent streams the OS image you picked onto the drive.
5. The agent installs the agent package into the new system, with the board's own credential.
6. The board boots from its drive and reports in.

Over the internet this takes about six minutes on a Compute Module 4 or 5 ([Installing an operating system](../install-an-os/)).

## What checks what

| Step | Checked by | How |
|---|---|---|
| Recovery image | Bootloader | RSA signature made with the server's own key. Each server creates its key when you turn network boot on |
| Agent in recovery | Bootloader | The agent is part of the signed image. Recovery downloads no code |
| OS image | Agent | SHA-256 sent with the install command. The agent keeps the first part of the image in memory and writes it last, so a drive whose checksum did not match never becomes bootable |
| Agent package | Server, then agent | Detached signature made on hardware keys kept offline. The server checks a release when it is imported, and the agent checks the package again before installing it |
| Commands and secrets | TLS | The device channel uses TLS whenever the server has an `https` address |

The keys that sign agent packages are built into the agent. A board therefore installs only agents signed by the keys of the build it already runs. If you build the server and the agent from source for your own fork, you replace that key set and sign your own releases ([ARTIFACT-SIGNING.md](https://github.com/uptime-lab/orchestrator/blob/main/docs/ARTIFACT-SIGNING.md)).

## Where the chain stops

- **This is not Secure Boot.** The bootloader's key is stored in the EEPROM, not fused into the board. Someone who holds the board, or has root on it, can write another key.
- **The installed OS boots unsigned.** The signature covers the recovery system. What you install afterwards is your image, and the board boots it as it is.
- **OS images are not signed.** The checksum protects against a damaged or swapped download only as far as the channel that carried it. On a server reached over plain HTTP on a local network, that channel is not encrypted.
- **The server is trusted.** Whoever controls your server controls your boards.

> **Note:** A server on a local network without a certificate sends commands and secrets unencrypted. Use it on a network you trust, or give the server a DNS name and let the installer get a certificate.

Next: [Adding a device](../add-a-device/).
