# Securing User Mode and Privileged Mode with Simple Passwords

# tested on i86bi-linux-l2-adventerprise-15.1b
from utils.base import execute_commands

connection_type = "telnet"

device = {
    "host": "172.16.59.128",
    "port": 32769,
}

commands = [
    "enable",
    "configure terminal",

    "interface vlan 1",
    "ip address 192.168.1.200 255.255.255.0",
    "no shutdown",
    "exit",

    "ip default-gateway 192.168.1.1",
    "ip name-server 8.8.8.8",
    "ip name-server 1.1.1.1",
    "exit",
    
    "show running-config",
    "show interface vlan 1",
]

execute_commands(device, connection_type, commands)