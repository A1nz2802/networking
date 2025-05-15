from netmiko import ConnectHandler
from typing import Dict, List, Literal

COLOR_YELLOW = '\033[93m'
COLOR_CYAN = '\033[96m'
COLOR_RESET = '\033[0m'

ConnectionType = Literal["telnet", "ssh"]

def execute_commands(device: Dict[str, str], connection_type: ConnectionType, commands: List[str]):

    device['device_type'] = "cisco_ios_telnet" if connection_type == "telnet" else "cisco_ios_ssh"

    net_connect = ConnectHandler(**device)

    print(f"\n{COLOR_YELLOW}Successfully connected to {device['host']} via {connection_type}.{COLOR_RESET}\n")

    for command in commands:
        output = net_connect.send_command(command, expect_string=r'#')
        print(f"{COLOR_CYAN}> {command}{COLOR_RESET}\n")
        print(output)
        print("\n")

# net_connect.disconnect()
