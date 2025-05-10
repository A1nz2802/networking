https://github.com/hegdepavankumar/Cisco-Images-for-GNS3-and-EVE-NG
requirements: https://developer.cisco.com/docs/modeling-labs/faq/#reference-platform-and-images-questions

| Image                                                            | Device Type       | Primary Layer | Comments                                            |
|------------------------------------------------------------------|-------------------|---------------|-----------------------------------------------------|
| i86bi-linux-l2-adventerprise-15.1b.zip                           | IOU L2 Switch     | Layer 2       | Traditional IOU switch.                             |
| cat9kv-17.10.01-prd7.tgz (Cisco Catalyst 9000v)                  | Cat9k Switch      | Layer 2/3     | Modern switch (IOS XE).                             |
| i86bi-linux-l3-jk9s-15.0.1.bin                                   | IOU L3 Router     | Layer 3       | IOU router for basic routing.                       |
| csr1000vng-universalk9.17.03.05-serial.tgz (Cisco CSR1000v 17.x) | CSR1000v Router   | Layer 3       | Modern router (IOS XE), also for SD-WAN.            |
| c2691-adventerprisek9-mz.124-15.T14.image                        | Cisco 2691 Router | Layer 3       | Classic router (Dynamips).                          |
| c3725-adventerprisek9-mz.124-15.T14.image                        | Cisco 3725 Router | Layer 3       | Classic router (Dynamips), more capable than c2691. |
| c7200-adventerprisek9-mz.153-3.XB12.image                        | Cisco 7200 Router | Layer 3       | High-performance router (Dynamips).                 |
| c8000v-17.06.03.tgz (Cisco Catalyst 8000V Edge)                  | C8000v Router     | Layer 3       | Modern router (IOS XE) for SD-WAN.                  |

ssh root@ip
telnet ip port
scp some-file.zip root@ip:/some/


# Configure ssh
sudo nano /etc/ssh/sshd_config

# Initial Eve-ng config

sudo apt update
sudo /opt/unetlab/wrappers/unl_wrapper -a fixpermissions

/opt/unetlab/addons/dynamips

.image and .image.md5sum -> dynamips
.bin -> addons/iol/bin
.qcow2 -> addons/quemu/respective_file_name/


