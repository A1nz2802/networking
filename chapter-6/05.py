# Configuring a Switch to Learn Its IP Address with DHCP.

# tested on `viosl2-adventerprisek9-m.ssa.high_iron_20200929` 
from utils.base import execute_commands

connection_type = "telnet"

device = {
    "host": "172.16.59.128",
    "port": 32771,
}

commands = [
    "enable",
    "configure terminal",

    "hostname mysw1",
    "ip domain name a1nzdev.com",
    "crypto key generate rsa",
    "1024",

    "ip ssh version 2",
    "line vty 0 1500",
    "login local",
    "transport input ssh telnet",
    "exit",

    "username a1nz secret rem3232",
    "username albedo secret ram1212",

    "show ip shh",
    "show ssh",
    "end",
]

execute_commands(device, connection_type, commands)
