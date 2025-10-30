# Configuring IPv4 on a Switch

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
    "interface vlan 1",
    "ip address 192.168.1.200 255.255.255.0",
    "no shutdown",
    "exit",

    "ip default-gateway 192.168.1.1",
    "ip name-server 8.8.8.8 8.8.4.4",
]

execute_commands(device, connection_type, commands)
