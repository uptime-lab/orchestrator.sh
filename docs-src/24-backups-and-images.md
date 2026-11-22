---
title: Backups and golden images
summary: Copy a node's drive to the server, put it back, or turn it into an image for other nodes.
section: Devices
---
Copy a node's drive to your server and put it back later, or turn a configured node into a golden image you install on other nodes. Both are taken while the node runs the recovery system.

## Back up a node's drive

1. Open the node, go to **Actions** and click **Reboot to recovery**. Wait until it shows **RECOVERY**.
2. Under **Provisioning**, click **Create backup**.
3. Type an **Image title**. Leave **Target Device** on **Boot disk (default)** unless the system lives on another drive.
4. Leave **Golden image** unticked and click **Create backup**.
5. Open **Command history** and wait until **Capture image** reads **SUCCESS**.
6. Click **Reboot**. The node starts its own system again, because **Reboot to recovery** lasts for one boot.

![The Create backup form on plasma-rig-01 with the title plasma-rig-01 baseline and Golden image unticked](img/backups-and-images/01-create-backup.jpg)

The capture checks the filesystem, shrinks it to its data, then reads and uploads the drive. The terminal is unavailable while it runs. A fresh Ubuntu on a 1 TB drive came to 1.8 GB and took about six minutes.

![Capture image at 34 percent with the message Capturing and uploading image](img/backups-and-images/02-capture-progress.jpg "A capture in progress")

The backup appears under **Operations** → **Backups**. Click it to see which node it was captured from, download it or delete it.

![The Backups tab listing plasma-rig-01 baseline, format ZST, 1.81 GB, with the note Backup of node plasma-rig-01](img/backups-and-images/03-backups-tab.jpg)

## Restore a backup

1. Reboot the node to recovery.
2. Under **Provisioning**, click **Restore from backup**.
3. In **Image**, pick the backup. Backups and golden images are listed after the OS images.
4. Pick the **Target Device** and click **Restore from backup**.
5. Read the confirmation and click **Restore from backup** again.
6. When **Command history** shows the install has finished, click **Reboot**.

![The Restore from backup confirmation: it erases /dev/nvme0n1 on plasma-rig-01 and writes plasma-rig-01 baseline over it](img/backups-and-images/04-restore-confirm.jpg)

> **Warning:** A restore erases the target drive. Everything written since the backup is lost.

The node stays in recovery after the restore until you reboot it. Check that **Properties** → **Boot behavior** reads **Local OS** before you do.

Restored onto the same node, a backup boots as that node. Restored onto a different node, the server strips the machine identity during the install so the copy doesn't clash with its source.

## Make a golden image and install it on other nodes

A golden image is a backup without the machine identity: machine-id, SSH host keys, the adoption file, network state and hostname. Set up one node the way you want every node, then capture it.

1. Reboot the configured node to recovery.
2. Click **Create backup**, give it a title and tick **Golden image**.
3. Click **Create backup** and wait for **SUCCESS**. The source node keeps its own identity.
4. Reboot the source node.
5. On each target node, follow [Installing an operating system](../install-an-os/) and pick the golden image in **Image**.

![The Create backup form with Golden image ticked](img/backups-and-images/05-create-golden.jpg)

Gold images are listed under **Operations** → **Gold images**.

## What a backup holds and where it lives

A backup covers the drive up to the end of the system partition, with free space trimmed, stored compressed. It restores onto a smaller or larger drive as long as the data fits. A drive with a partition after the system partition can't be captured.

Backups and golden images live in your server's image storage, on local disk or in the bucket if the server uses object storage. They count toward the image limits set by whoever runs the server (`IMAGE_MAX_PER_ACCOUNT`, `IMAGE_MAX_BYTES_PER_ACCOUNT`, `IMAGE_MAX_BYTES_INSTANCE` in [CONFIGURATION.md](https://github.com/uptime-lab/orchestrator/blob/main/docs/CONFIGURATION.md)). Nothing deletes them for you.

## Who can do this

Admins can create and restore backups. Downloading or deleting an image needs the account's super admin. A backup carries the node's credentials, so treat a downloaded copy as a secret.
