from netmiko import ConnectHandler

# tested on i86bi-linux-l2-adventerprise-15.1b
device = {
    "device_type": "cisco_ios_telnet",
    "host": "172.16.59.128",
    "port": 32769,
}

net_connect = ConnectHandler(**device)

commands = [
    "show version",
    "show clock"
]

separator = "----- END COMMAND -----"

for command in commands:
    output = net_connect.send_command(command)
    print(f"Command: {command}\n")
    print(output)
    print(separator)
    print("\n")

# net_connect.disconnect()
