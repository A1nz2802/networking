## Configuring IPv4 on a switch

- **Step 1.** Use the interface vlan 1 command in global configuration mode to enter interface VLAN 1 configuration mode.
    ```bash
    mysw1# configure terminal
    mysw1(config)# interface vlan 1
    mysw1(config-if)# 
    ```

- **Step 2.** Use the ip address ip-address mask command in interface configuration mode to assign an IP address and mask.
    ```bash
    mysw1(config-if)# ip address 192.168.1.200 255.255.255.0
    ```

- **Step 3.** Use the no shutdown command in interface configuration mode to enable the VLAN 1 interface if it is not already enabled.
    ```bash
    mysw1(config-if)# no shutdown
    ```

- **Step 4.** Add the ip default-gateway ip-address command in global configuration mode to configure the default gateway.
    ```bash
    mysw1(config-if)# exit
    mysw1(config)# ip default-gateway 192.168.1.1
    ```

- **Step 5.** (Optional) Add the ip name-server ip-address1 ip-address2 … command in global configuration mode to configure the switch to use Domain Name System (DNS) to resolve names into their matching IP address and check config.
    ```bash
    mysw1(config)# ip name-server 8.8.8.8
    mysw1(config)# ip name-server 1.1.1.1
    mysw1(config)# show running-config
    mysw1(config)# show interfaces vlan 1
    ```

## Configuring a Switch to Learn Its IP Address with DHCP
- **Step 1.** Enter VLAN 1 configuration mode using the interface vlan 1 global configuration command, and enable the interface using the no shutdown command as necessary.
    ```bash
    mysw2(config)# interface vlan 1
    ```
- **Step 2.** Assign an IP address and mask using the ip address dhcp interface subcommand.
    ```bash
    mysw2(config-if)# ip address dhcp
    mysw2(config-if)# no shutdown
    mysw2(config-if)# ^Z
    ```
- **Step 3.** Check dhcp config
    ```bash
    mysw2(config)# show dhcp lease
    ```

> [!WARNING]
> Commands **show dhcp lease** and **show ip default-gateway** are not supported in Packet Tracer. 

## Configuring Speed, Duplex, and Description

```bash
mysw1# show interfaces status
mysw1# configure terminal
mysw1(config)# interface Fa0/1
mysw1(config-if)# duplex full
mysw1(config-if)# speed 100
mysw1(config-if)# description Printer on 3rd floor, Preset to 100/full
mysw1(config-if)# ^Z

mysw1(config)# interface range FastEthernet 0/2 - 5
mysw1(config-if-range)# description end-users connect here 
mysw1(config-if-range)# ^Z 
```