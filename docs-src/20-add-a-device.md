---
title: Adding a device
summary: Turn a Raspberry Pi into a managed node, then approve it.
section: Devices
---
Adopt a device so it shows up in **Nodes** and you can manage it. Open **Nodes**, click **Add node**, and pick the tab that fits your device.

| Your device | Tab |
|---|---|
| Already runs a 64-bit Debian or Ubuntu | **One command** |
| A board you can connect over USB in boot mode | **USB flash** |
| Blank, and you can put a card into it | **Master image** (provisioning card) |

The device needs Ethernet and outbound access to the server on port 50051, plus port 80 for a server on your local network or 443 for one on the internet. The USB and card ways bring their own recovery system, so you install an OS afterwards ([Installing an operating system](../install-an-os/)).

![Clicking Add node on the Nodes page and stepping through the One command, USB flash and Master image tabs of the panel that opens](img/add-a-device/v1-add-node-tabs.mp4 "The three ways to add a device")

## Run one command on a device that already runs Linux

![The One command tab with an empty Token name field, the Credentials users box, the collapsed Console login section and the Generate command button.](img/add-a-device/03-one-command.jpg)

1. Open the **One command** tab.
2. Type a **Token name** if you want one, such as `workshop batch`.
3. Click **Generate command**, then **Copy command**.
4. Run the line on the device as a user with sudo.

The script installs the agent and tells you when it has connected. On a fresh system it first waits for the system's own package upgrade to finish and tells you so. The device needs arm64 with `systemd`, `dpkg`, `curl` or `wget`, and `openssl`.

The token works for 7 days and for several devices. You find it under **Secrets** → **Tokens** ([Secrets and variables](../secrets-and-variables/#manage-tokens-for-new-devices)). To remove the agent later, run `curl -fsSL <server address>/uninstall.sh | sudo sh` with the same `http://` or `https://` address as in the install command.

## Flash a board from the browser

This writes the board's bootloader so it boots from your server. Use Chrome or Edge over HTTPS. On Windows, install the WinUSB driver first as the tab explains.

![The USB flash tab with the Connect device button, an empty Board serial field, the Node name field, the yellow flashing warning, the line Power the device on within 30 days of flashing, and a disabled Flash EEPROM button.](img/add-a-device/04-usb-flash.jpg)

1. Put the board into USB boot mode and connect it to your computer.
2. Click **Connect device** and pick the board. **Board serial** fills in.
3. Type a **Node name** if you want one.
4. Click **Flash EEPROM** and don't unplug the board until the green notice appears.
5. Unplug USB, connect Ethernet and power the board on.

The node arrives already approved. Power the board on within the days the tab names (30 by default). Until the board first connects, your account holds its serial only that long. After that another account can claim the serial. The node stays and binds the board when it connects, unless another account has claimed it first.

## Boot a blank device from a provisioning card

![The Master image tab: description of the FAT32 MBR requirement with the macOS scheme Master Boot Record, the GPL source note, the yellow keep-the-card-in warning, and the Name field set to sd-provisioning.](img/add-a-device/05-master-image.jpg)

1. Open the **Master image** tab.
2. Pick an **SSH key** for the new nodes, and set **Expires At** if 7 days is wrong for you.
3. Click **Download SD Image**. Each click creates a new token.
4. Format the card as FAT32 on an MBR partition table. In macOS Disk Utility, choose **View** → **Show All Devices**, select the card itself, and erase it as **MS-DOS (FAT)** with scheme **Master Boot Record**.
5. Unzip the bundle into the root of the card.
6. Insert the card and power the device on.
7. Leave the card in until you have approved the node and it shows **RECOVERY**. Then move the card to the next device.

To prepare a card for one named device, use the **Single node** tab instead. Create the node, then click **Download SD image** in its panel. That node arrives already approved.

> **Warning:** Treat a provisioning card as a secret. It can enrol devices into your account, and every device it sets up leaves a credential on it.

> **Warning:** A device that another server managed boots its own drive before the card, so it never reads your card. Remove the drive while the card does its work, or flash the board from the browser.

## Approve it

A device from **One command** or **Master image** shows a yellow bar and **PENDING** in **Nodes**. Click it, check the **HW serial**, and click **Approve**. Approval applies the node's access and utilities at once. By default, a device running the recovery system from a provisioning card also gets a bootloader that boots from your server. A device added with **One command** keeps its bootloader.

![The doomsday-clock panel with the Pending Approval banner, its explanation, the Approve and Reject buttons, and the node's IP, MAC and hardware serial.](img/add-a-device/08-approve.jpg)

Next: [install an operating system](../install-an-os/) on the node.
