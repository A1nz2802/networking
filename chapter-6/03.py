# Securing User Mode Access with Local Usernames and Passwords

# tested on i86bi-linux-l2-adventerprise-15.1b
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
    "username a1nz secret rem3232",
    "username albedo secret ram1212",

    "ip domain name a1nzdev.com",
    "crypto key generate rsa",
    "1024",

    "ip ssh version 2",
    "line vty 0 15",
    "login local",
    "transport input ssh",
]

execute_commands(device, connection_type, commands)