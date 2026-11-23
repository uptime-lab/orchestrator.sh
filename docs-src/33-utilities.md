---
title: Utilities: managed software
summary: Assign built-in software to a unit and keep it installed and configured.
section: Operating a fleet
---
A utility is software from a built-in catalog that the platform installs and keeps configured on every node its assignment reaches. Which nodes those are is decided by the unit rules on [Organizational units and policies](../organization/).

## Assign a utility to a unit

1. Open **Utilities** and the **Assignments** tab.
2. Select the unit in the left rail.
3. Click **Assign utility** and pick one.
4. Set the parameters in the panel that opens.
5. Click **Save**.
6. Click **Apply**.

![With Basement selected in the rail, clicking Assign utility: the dialog says the new assignment starts scoped to Basement, the list scrolls to Security updates and its Assign button, and the dialog is closed with Cancel](img/utilities/v1-assign-utility.mp4 "Pick a utility for a unit")

![The Security updates assignment on Garage with Enabled, its parameters, and the Save and Apply buttons](img/utilities/08-security-updates-config.jpg)

**Apply** sends what is saved, so save first. Online nodes get it at once and offline nodes when they reconnect. A node you approve later gets its unit's utilities at once.

Text parameters can use `{{secrets.NAME}}` for variables and `{{node.attributes.KEY}}`. A secret is refused, because a utility's settings can be read back from the device.

A node needs its installed OS, a Debian-based system and agent 0.6.5 or newer to receive utilities.

## See whether it applied

Open the node, then **Properties → Utilities**.

![The Utilities view of a node showing Security updates from Garage with an APPLIED badge](img/utilities/05-node-utilities-applied.jpg)

**applied** means the device confirmed this configuration. **update pending** means it changed since, **declared** means it was never applied, and **failed** shows the reason on hover. **Apply now** resends this node's whole set.

## Remove an assignment

Click **Delete** on the assignment. The software stays installed and keeps running, and the platform stops managing it. To uninstall it, run a [playbook](../playbooks/).

Clear **Enabled** and save to pause an assignment without losing its settings.

## What's in the catalog

- **Docker**: the Docker engine, with log rotation. Members of the `docker` group are effectively root.
- **Kiosk display**: one web page fullscreen on HDMI. Brings Docker along.
- **Metrics exporter**: Prometheus node exporter on port 9100, without authentication.
- **Storage endurance**: less SD-card wear, with zram swap and a journal cap.
- **Tailscale VPN**: joins your tailnet. Use a short-lived auth key.
- **Security updates**: automatic security updates. It never reboots, so reboot yourself after a kernel update.
- **ZeroTier network**: joins a ZeroTier network.

## Example: put a dashboard on a screen

1. On **Secrets**, create a variable `KIOSK_URL` with the dashboard address and attach it to the unit.
2. On **Utilities**, select the unit and assign **Kiosk display**.
3. Set **URL** to `{{secrets.KIOSK_URL}}`, leave **Kiosk image** on the default and click **Save**.
4. Click **Apply**.
5. On a node with a screen, open **Properties → Utilities** and check that **Kiosk display** shows **applied**.

![The Kiosk display assignment panel with URL set to {{secrets.KIOSK_URL}} and the default kiosk image](img/utilities/04-kiosk-config.jpg)

A changed `KIOSK_URL` reaches the screens at the next **Apply**. To show another page on one screen, assign the kiosk to that node too. The node's assignment wins.

Next: [Status, attention and the audit trail](../status-and-audit/).
