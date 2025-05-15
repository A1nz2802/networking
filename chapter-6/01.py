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
    "enable secret love",

    "interface vlan 1",
    "ip address 192.168.1.3 255.255.255.0",
    "no shutdown",
    "exit",

    "line console 0",
    "password faith",
    "login",
    "exit",

    "line vty 0 4",
    "transport input telnet",
    "password hope",
    "login",
    "end",
    "copy running-config startup-config",
]

execute_commands(device, connection_type, commands)
