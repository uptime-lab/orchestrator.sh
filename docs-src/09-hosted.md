---
title: Quick start on the hosted service
summary: Sign up, add a board with one command and boot it from the network. No server to install.
section: Start
---
We run the server at [app.orchestrator.sh](https://app.orchestrator.sh). An account is free for 10 devices. To run the server on your own machine instead, see [Quick start on your own server](../quick-start/).

## What you need

- A Raspberry Pi 4, Pi 5, Compute Module 4 or Compute Module 5 on wired Ethernet.
- Outbound access from the board to `app.orchestrator.sh` on ports 443 and 50051, and to `boot.orchestrator.sh` on port 80 for network boot. Nothing has to be opened towards the board.

## Sign up

Open [app.orchestrator.sh](https://app.orchestrator.sh) and click **Sign up with Google**. That's it.

Prefer a password? Sign up with your e-mail and click the link in the confirmation message. Until you do, the app shows a reminder instead of your account.

Once you're in, you can add a passkey under your account settings and sign in with it from then on.

## Add a board that already runs Linux

1. Click **Add node** and open the **One command** tab.
2. Click **Generate command**, then **Copy command**.
3. Run the line on the board as a user with sudo. It needs 64-bit Raspberry Pi OS, Debian or Ubuntu.
4. The board shows up in **Nodes** as **PENDING**. Check the **HW serial** and click **Approve**.

A board with nothing on it joins another way: flash its bootloader from the browser over USB, or boot it from a provisioning card ([Adding a device](../add-a-device/)).

## Make it boot from the network

A board added with one command keeps its old bootloader. Point it at the server once:

1. Open the node, go to **Advanced** → **Bootloader / EEPROM** and click **Update bootloader**.
2. Click **Reboot to apply**.

From now on the board asks the server first on every boot. The server sends the recovery system when you ask for it, and otherwise the board boots its own drive. If the server can't be reached, the board also boots its own drive.

## Install an operating system

1. Go to **Operations** → **Install images** and upload an image. A hosted account holds up to 3 images of up to 15 GB each.
2. Open the node, click **Reboot to recovery** and wait for **RECOVERY**.
3. Follow [Installing an operating system](../install-an-os/) from step 3.

## More than 10 devices

Write to [sales@orchestrator.sh](mailto:sales@orchestrator.sh). Devices you already added keep working when a limit is reached. Only new ones wait.

Next: [Adding a device](../add-a-device/).
