# Securing User Mode Access with Local Usernames and Passwords

# tested on i86bi-linux-l2-adventerprise-15.1b
from utils.base import execute_commands

connection_type = "telnet"

device = {
    "host": "172.16.59.128",
    "port": 32770,
}

commands = [
    "enable",
    "configure terminal",
    "username a1nz secret rem3232",
    "username albedo secret ram1212",

    "line console 0",
    "login local",
    "no password",
    "exit",

    "line vty 0 4",
    "login local",
    "no password",
    "end",
]

execute_commands(device, connection_type, commands)