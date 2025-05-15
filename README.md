## Requirements:

**Source Repository:** Images listed below were obtained from [https://github.com/hegdepavankumar/Cisco-Images-for-GNS3-and-EVE-NG](https://github.com/hegdepavankumar/Cisco-Images-for-GNS3-and-EVE-NG).

| Image                                                              | Device Type       | Layer  | Key Information                                                |
|:-------------------------------------------------------------------|:------------------|:-------|:---------------------------------------------------------------|
| `i86bi-linux-l2-adventerprise-15.1b.zip`                           | IOU L2 Switch     |  L2    | Basic Layer 2 IOU switch.                                      |
| `cat9kv-17.10.01-prd7.tgz` (Cisco Catalyst 9000v)                  | Cat9k Switch      |  L2/3  | Modern IOS XE switch, supports L2/L3. Higher resource usage.   |
| `i86bi-linux-l3-jk9s-15.0.1.bin`                                   | IOU L3 Router     |  L3    | Basic Layer 3 IOU router.                                      |
| `csr1000vng-universalk9.17.03.05-serial.tgz` (Cisco CSR1000v 17.x) | CSR1000v Router   |  L3    | Modern IOS XE router, also for SD-WAN. Higher resource usage.  |
| `c2691-adventerprisek9-mz.124-15.T14.image`                        | Cisco 2691 Router |  L3    | Classic Dynamips router, simpler scenarios.                    |
| `c3725-adventerprisek9-mz.124-15.T14.image`                        | Cisco 3725 Router |  L3    | Classic Dynamips router, more capable than c2691.              |
| `c7200-adventerprisek9-mz.153-3.XB12.image`                        | Cisco 7200 Router |  L3    | High-performance Dynamips router.                              |
| `c8000v-17.06.03.tgz` (Cisco Catalyst 8000V Edge)                  | C8000v Router     |  L3    | Modern IOS XE router for SD-WAN. Higher resource usage.        |
| `linux-centos-8.tgz`                                               | Linux Node        |  N/A   | CentOS 8 based Linux node for simulating hosts/servers/tools.  |
| `linux-debian-10.3.0.tgz`                                          | Linux Node        |  N/A   | Debian 10 based Linux node for simulating hosts/servers/tools. |
| `linux-ubuntu-21.04-desktop.tgz`                                   | Linux Node        |  N/A   | Ubuntu Desktop 21.04 based Linux node, higher resource usage.  |

**Official image and platform requirements:** [https://developer.cisco.com/docs/modeling-labs/faq/#reference-platform-and-images-questions](https://developer.cisco.com/docs/modeling-labs/faq/#reference-platform-and-images-questions)

## How to Copy Files to the EVE-NG VM

Here are common methods to transfer files from your host machine to the virtual machine (VM) where EVE-NG is installed. Replace `<ip>` with the IP address of your EVE-NG VM.

* **Using SSH (Secure Copy - `scp`):** This is the most secure and recommended method.

    ```bash
    scp <local_file_path> root@<eve-ng_ip>:<remote_directory_path>/
    ```

    Example to copy `some-file.zip` to the `/root/` directory on the EVE-NG VM:

    ```bash
    scp some-file.zip root@192.168.1.100:/root/
    ```

* **Using Telnet (for simple text-based configurations - less secure):** While possible for very basic text configurations, it's generally not recommended for file transfer due to its lack of security.

    ```bash
    telnet <eve-ng_ip> <port> # Requires a service running on the EVE-NG VM to handle the transfer.
    ```

* **Using SCP from within the EVE-NG VM:** You can also initiate a transfer from the EVE-NG VM itself if it has network access to your host.

    ```bash
    scp root@<host_ip>:<local_file_path> <remote_directory_path>/
    ```

## Configuring SSH on Linux Nodes in EVE-NG

To enable SSH on a Linux node within EVE-NG, you typically need to install and configure the SSH server.

```bash
# Update package lists
sudo apt update

# Install the OpenSSH server (for Debian/Ubuntu)
sudo apt install openssh-server

# For CentOS
# sudo yum install openssh-server

# Edit the SSH server configuration file
sudo nano /etc/ssh/sshd_config
```

In the `sshd_config` file, you can modify settings like the listening port (default is 22), permitted root login, and authentication methods. **Remember to restart the SSH service after making changes:**

```bash
# For Debian/Ubuntu
sudo systemctl restart sshd

# For CentOS
# sudo systemctl restart sshd
```

## Initial EVE-NG Configuration

These are some initial commands that might be useful for setting up your EVE-NG environment.

```bash
# Update package lists
sudo apt update

# Fix permissions issues within the EVE-NG lab directory
sudo /opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

## Image Placement in EVE-NG

Place the downloaded image files in the following directories within your EVE-NG VM:

* **.image and .image.md5sum files (for Dynamips-based routers):** `/opt/unetlab/addons/dynamips/`
* **.bin files (for IOU - IOS on Linux):** `/opt/unetlab/addons/iol/bin/`
* **.qcow2 files (for Qemu-based VMs like Linux nodes and modern Cisco devices):** `/opt/unetlab/addons/quemu/<respective_file_name>/` (create the subdirectory if it doesn't exist)

> [!IMPORTANT]
> After adding new images, you might need to fix permissions again.

## How to Execute Python Scripts

These steps outline how to set up a virtual environment and run Python scripts (like those using Netmiko) on a Linux node within EVE-NG.

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate.fish

# Install the Netmiko library
pip install netmiko

# Run your Python script
python -m chapter-6.01

# Deactivate the virtual environment when you're done
deactivate
```