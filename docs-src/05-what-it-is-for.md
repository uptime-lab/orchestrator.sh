---
title: What it is for
summary: What Uptime Orchestrator does and who uses it, from one board at home to screens across many sites.
section: Start
---
Uptime Orchestrator installs, reaches and repairs Raspberry Pi boards over the network. A board boots from the server, so you can put an operating system on it, open a terminal on it and bring it back when its system no longer starts, without a keyboard, a card reader or a trip to the device.

## The problem

A Raspberry Pi is easy to set up on a desk and hard to look after once it is somewhere else. A card wears out, an update breaks the boot, SSH stops answering, and someone has to go there with a laptop. With one board that is an evening. With boards in other buildings or other cities it is a cost you pay every time.

With Orchestrator the board asks the server first on every boot. From the browser you can:

- install or reinstall the operating system on a board with an empty or broken drive
- open a root terminal when SSH is gone
- back up a drive and restore it later
- set users, keys, software and schedules once and have every board keep them

The board connects out to the server. It can sit behind a home router or a customer's firewall, and nothing has to be opened towards it.

## Who uses it

### One board

A home server, a home automation box, a Pi at a relative's house, a camera in a shed. If its system stops booting you switch it to recovery from your browser and reinstall it or restore a backup. Turn on the watchdog and a board that hangs reboots by itself.

### A homelab or a cluster

A shelf of boards or a rack of Compute Modules. Install the same image on a new board in minutes, capture a configured board as a golden image, and reinstall a node instead of debugging it. Hardware profiles cover carrier boards, the Compute Blade included.

### A classroom or a lab

A set of boards that many people use and break. Keep one golden image and put each board back to it before the next class. Give a group its own users and SSH keys by placing its boards in a unit, and take them away the same way.

### Kiosks and screens

Displays in cafés, shops, offices and airports, and kiosks spread over many sites. Assign the kiosk display to a unit and its boards keep it installed. Give each site its own unit, run playbooks on a schedule, and bring a screen back from recovery without sending anyone to it.

### A company's devices

Edge boxes at customer sites, test rigs, gateways. Roles decide who may do what, single sign-on and two-step verification protect the accounts, every command is logged with its sender, and the API lets your own scripts do what the web UI does. You can run the server on your own machine.

## What you need

A Raspberry Pi 4, Pi 5, Compute Module 4 or Compute Module 5 on wired Ethernet.

- On our server: [Quick start on the hosted service](../hosted/). Free for 10 devices.
- On your own machine: [Quick start on your own server](../quick-start/). Free for 25 devices.

To see how a board boots from the server, read [How it works](../how-it-works/).
