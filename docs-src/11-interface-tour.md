---
title: A tour of the interface
summary: Where each section is and how to read the Nodes list.
section: Start
---
Find your way around the web UI. The list below links each top-level section to its page in this guide.

![The Nodes page: top navigation, the Organizational Units sidebar on the left and the table of twelve nodes](img/interface-tour/01-nodes-page.jpg)

## Where things are

- **Nodes** lists your devices. Click a row to open its panel ([The node panel](../node-panel/)), or click **Add node** to adopt one ([Add a device](../add-a-device/)).
- **Organization** holds your units and the policies they set ([Organization and units](../organization/)).
- **Credentials** controls who can log in to devices ([Access and credentials](../access-and-credentials/)).
- **Secrets** holds values for devices and playbooks, and adoption tokens ([Secrets and variables](../secrets-and-variables/)).
- **Operations** has playbooks and their runs ([Playbooks](../playbooks/)) and your OS images ([Install an operating system](../install-an-os/)).
- **Utilities** keeps software such as security updates configured on nodes ([Utilities](../utilities/)).
- **Status** lists nodes that need you and the command history ([Status and audit](../status-and-audit/)).
- The round badge at the top right opens your password, sign-in settings and team ([Team and security](../team-and-security/)).

The **Organizational Units** sidebar on the left filters most pages to one unit. You create and rename units on the **Organization** page.

## Read a node's status

The coloured bar at the left of each row and the word under the name give the node's status.

| Colour | Status |
|---|---|
| Green | **ONLINE** |
| Violet | **RECOVERY**, the network-boot recovery system |
| Yellow with **PENDING** | **AWAITING APPROVAL** |
| Yellow | Restarting, installing an OS, shutting down, ready for adoption |
| Orange | **MAINTENANCE**, a command is running |
| Blue | **FLASHING** the bootloader, or **BUSY** |
| Red | **OFFLINE**, or the last adoption or OS install failed |
| Grey | **UNREACHABLE**, or **ADOPTING** |

Hover over a badge next to a name, such as **REBOOT PENDING** or **UNDER-VOLTAGE**, to see what it means.

## Find a node

Type in the search box to match a name, IP address, serial, OS or notes. The dropdowns narrow by status, board, RAM and disk, and they combine with the unit selected in the sidebar.

![Typing rocket into the search box leaves rocket-bench-01 and rocket-bench-02; after clearing it, choosing Offline in the status filter leaves secret-lair-door and welding-bot, then the filter goes back to All statuses](img/interface-tour/v1-filter-nodes.mp4 "Search and filter the node list")

Every live node falls under one of **Online**, **Recovery**, **Maintenance** or **Offline**, so if a node seems missing, step through them.

## Move nodes into a unit

1. Click **Select / Assign to unit** next to the page title.
2. Tick the nodes, or click **Select all**.
3. Open **Assign to unit** and pick a unit, or **Remove from unit (Unassigned)**.
4. Click **Done**.

In selection mode you can also drag the ticked nodes onto a unit in the sidebar. **Actions** in the same toolbar reboots, runs a playbook on, or deletes the selected nodes.

![Selection mode in the Garage unit: two nodes ticked and the Assign to unit menu open, listing Laboratory, Test bench, Garage, Basement and Remove from unit](img/interface-tour/05-select-assign.jpg)
