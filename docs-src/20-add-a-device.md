---
title: Adding a device
summary: The four ways to turn a Raspberry Pi-class board into a managed node, what each dialog asks for, and what happens on the device afterwards.
section: Devices
---
A device becomes a node when its agent connects to the platform. This page covers the four ways to get there and what you see until the node is ready for an operating system.

## Before you start

- The board must be in the supported list below and wired to the network over Ethernet. Wi-Fi is not part of the supported path.
- The device needs outbound access to the platform: HTTPS (443) and the agent port (50051 by default). Nothing has to reach the device from outside.

| Board | Status |
|---|---|
| Compute Module 4 | Validated |
| Compute Module 5 Lite | Validated |
| Raspberry Pi 5 | Validated, including the network-boot recovery round trip |
| Raspberry Pi 4 B | Partially validated: network-boot recovery proven, SD-card adoption not yet run |
| Compute Module 5 (with eMMC) | Expected to work, not validated |
| CM4S | Best effort, untested |
| Pi 400 | Incidental: covered by the Pi 4 class, not tested |

## Which way to choose

Open **Nodes** and click **Add node**. The panel has four tabs.

| Your device | Use | Arrives |
|---|---|---|
| Already runs a 64-bit Debian or Ubuntu | **One command**: one line pasted on the device | pending approval |
| A Compute Module 4 or 5 you can put into USB boot mode next to your computer | **USB flash**: write the bootloader from the browser (Chrome or Edge only) | approved |
| Blank, and you want to prepare one card for one named node | **Single node**: create the node, then download its own SD image | approved |
| Blank, and you want one card for a batch of devices | **Master image**: one SD provisioning bundle for many devices | pending approval |

The card and USB paths bring their own recovery system, so the device needs no OS. Afterwards you install one from the platform: [Installing an operating system](../install-an-os/).

> **Note:** A self-hosted install on the devices' own network can show a fifth tab, **Via SSH**, not covered here.

## One command (a device that already runs Linux)

![The One command tab with an empty Token name field, the Credentials users box, the collapsed Console login section and the Generate command button.](img/add-a-device/03-one-command.jpg "One command: name the token, then generate the install line.")

1. Open the **One command** tab.
2. **Token name (optional)**: a label for the token this creates, such as `workshop batch`. Left empty, it is named after today's date.
3. Click **Generate command**. The panel shows a line under **Run on the device**, with **Copy command** below it.
4. Run that line on the device as a user with sudo. It has the form `curl -fsSL https://<your platform>/install.sh | sudo sh -s -- --token '<token>'`.

The token inside expires in 7 days and can adopt several devices. Each click on **Generate command** creates another token; manage them under **Secrets → Tokens** ([Secrets and variables](../secrets-and-variables/#tokens)).

The device must be arm64 with a Debian-based system (`systemd`, `dpkg`, `curl` or `wget`, `openssl`) and a Raspberry Pi serial number. The script installs and verifies the agent, then waits for it to connect and prints `OK: agent connected`. The node appears **Awaiting approval** (see [Approving a device](#approving-a-device)).

> **Note:** On a freshly installed Ubuntu, the system's own first-boot package upgrade can hold the package lock for up to about half an hour. In 0.1.0 the script prints `Another package operation is running; waiting for it (up to 5 minutes)...`, and if the lock outlasts those five minutes it stops with a lock error. Nothing is broken: run the same command again once the upgrade has finished; the token stays valid. Release 0.1.1 waits for the upgrade instead.

To remove the agent later: `curl -fsSL https://<your platform>/uninstall.sh | sudo sh`.

## USB flash (a Compute Module next to your computer)

This writes the board's bootloader (EEPROM) from your browser so the board boots from the network on its own. It needs Chrome or Edge and HTTPS; other browsers see a notice and an **Open Master image** button instead.

![The USB flash tab with the Connect device button, an empty Board serial field, the Node name field, the yellow flashing warning and a disabled Flash EEPROM button.](img/add-a-device/04-usb-flash.jpg "USB flash: connect the board in USB boot mode, then write its bootloader.")

1. Put the board into USB boot mode (`nRPI_BOOT`) and connect it to your computer over USB.
2. Click **Connect device** and pick the board in the browser's USB picker. The button changes to **Connected** with the chip type, and **Board serial** fills itself in.
3. **Node name (optional)**: empty gives a generated name.
4. Click **Flash EEPROM**. A log shows each step, and a green notice confirms the flash and names the node.

The node appears as **Flashing**, then **Ready for Adoption**; its panel says the device will netboot and come online already approved. Disconnect USB, connect Ethernet and power the board on.

> **Warning:** Do not disconnect or cut power while the flash runs.

> **Warning:** Power the board on within 30 days of flashing (`NODE_SERIAL_LEASE_DAYS` on a self-hosted install). After that the node gives up its claim on the board's serial: it stays in the list, but the device will not join it until you flash it again. The dialog does not mention this limit.

> **Note:** On Windows the board needs the WinUSB driver first; the tab explains how. macOS and Linux need none.

## Single node (one card for one named device)

![The Single node tab: Node Name field, SSH key selector showing Workshop laptop (Default), and the Credentials users box.](img/add-a-device/01-single-node.jpg "Single node: the node record exists before the device does.")

1. Open **Single node** (the default tab) and type a **Node Name**, for example `jetpack-test-04`.
2. **SSH key (optional)**: **No key — attach later** is fine.
3. Leave **Network-first** ticked if the device should boot from the network from now on. The platform then rewrites the bootloader on the device's first boot, and the device reboots once during onboarding.
4. Click **Create Node**. The node's panel opens.

![The lower half of the Single node tab: Console username and password fields, the ticked Network-first checkbox, Create Node and Cancel.](img/add-a-device/02-single-node-options.jpg "The console login fields and the network-first choice.")

The new node (**Ready for Adoption**) offers **Download SD image** in its panel: a bundle of about 90 MB with this node's own token. Unzip it onto a card prepared as in [Preparing the card](#preparing-the-card) and boot the device from it; it binds to this node already approved. The panel also shows an install command for this node, for a device that already runs Linux.

## Master image (one card for many devices)

This is the SD provisioning bundle: a ZIP with the recovery system and a newly created master token.

![The Master image tab: description of the FAT32 MBR requirement, the GPL source note, the yellow keep-the-card-in warning, and the Name field set to sd-provisioning.](img/add-a-device/05-master-image.jpg "Master image: one bundle provisions any number of devices.")

![The rest of the Master image form: SSH key with its hint, the Credentials users box, Console login, Expires At date field and the Download SD Image button.](img/add-a-device/06-master-image-fields.jpg "The bundle's options and the download button.")

- **Name**: the name of the master token inside the bundle (default `sd-provisioning`).
- **SSH key**: the key assigned to nodes provisioned with this bundle.
- **Expires At (optional)**: the token stops working at the end of that day. Left empty, it expires after 7 days.
- **Download SD Image** creates the token and downloads the ZIP. Each click creates a new token.

Unzip the bundle into the root of the card, insert it and power the device on. It boots the recovery system from the card and appears **Awaiting approval**. Keep the card in until the node is approved; the same card then serves the next device.

### Preparing the card

> **Warning:** The card must be FAT32 on an MBR partition table, with the FAT volume as the first partition. A card erased on macOS with the default GUID scheme starts with a small EFI partition. Older boards do not boot it at all; newer ones (Compute Module 5, Pi 5) boot the recovery system and then never reach the server: the screen shows a login prompt and the node never appears.

On macOS, in Disk Utility:

1. Choose **View → Show All Devices**.
2. Select the card itself, not the volume on it.
3. Click **Erase**, choose format **MS-DOS (FAT)** and scheme **Master Boot Record**.
4. Unzip the bundle onto the card again.

> **Warning:** Treat a provisioning card as a secret. It carries a token that can enrol devices into your account, and every device it provisions leaves its own credential on the card. Do not leave it in a drawer or hand it on.

> **Warning:** A device that another server managed before tries network, then NVMe, then USB, then SD. If its drive holds a bootable system, it boots that and never reads your card. Remove the drive while the card does its work, or use **USB flash**, which replaces the old bootloader.

## Console login

Every tab lists the users from [Credentials](../access-and-credentials/) that will be applied to the node, and has a collapsed **Console login (optional)** section: a local account for UART or a keyboard, for when the network or agent is down. Credentials does not manage it. Leave both fields empty for none.

## Approving a device

Devices adopted with a master token (**One command** and **Master image**) wait for approval. **Single node** and **USB flash** nodes are created by you in advance and arrive approved.

![Two node list rows: backup-vault with a red offline bar, and doomsday-clock with a yellow bar, a PENDING badge and AWAITING APPROVAL under its name.](img/add-a-device/07-pending-row.jpg "A device waiting for approval: yellow bar and PENDING badge.")

A waiting node has a pulsing yellow bar, a **PENDING** badge and **Awaiting approval**; it also appears on [Status → Attention](../status-and-audit/). It receives no commands until approved.

![The doomsday-clock panel with the Pending Approval banner, its explanation, the Approve and Reject buttons, and the node's IP, MAC and hardware serial.](img/add-a-device/08-approve.jpg "Approve or reject from the node's panel.")

Click the node. Its panel shows the **Pending Approval** banner with **Approve** and **Reject**, and the device's IP, MAC and **HW serial** so you can tell which board is asking. A rejected node can be approved later. An approved device counts toward the server's limit of 25 free devices ([The device limit](../team-and-security/#the-device-limit)).

![Account defaults, Boot card: Target set to System default (Recovery), and Auto-flash EEPROM on approval set to System default (on), each with its explanation.](img/add-a-device/10-auto-flash.jpg "Organization → Account defaults: the bootloader is flashed on approval by default.")

What approval triggers depends on **Auto-flash EEPROM on approval** under **Organization → Account defaults** or the node's unit ([Organization](../organization/)); it is on by default. For a device running the recovery system from its card, approving then writes a per-device bootloader that boots from the network first. The device reboots into the recovery system over the network. Once the node shows **Recovery**, take the card out. A **One command** device runs its own OS, so approval flashes nothing.

## What a new node looks like

![The plasma-rig-01 row with a violet bar and RECOVERY status; its hostname begins with rpi- and its OS column reads Buildroot.](img/add-a-device/09-recovery-row.jpg "A node booted into the recovery system over the network.")

A node booted over the network glows violet and reads **Recovery**: its hostname ends in `-recovery`, the OS column shows the recovery system (Buildroot), and live metrics work. That is normal for a device with no installed OS. A **One command** node shows green and **Online** instead.

## Next steps

- [Installing an operating system](../install-an-os/) on a recovery node.
- [The node panel](../node-panel/): tabs, commands and terminal.
- [Organization](../organization/): move the node into a unit to pick up its policies.
