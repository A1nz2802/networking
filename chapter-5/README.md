# MAC Address Learning Lab

This lab was tested with the following images:
- `Linux-ubuntu-server-20.04` (Linux host)
- `viosl2-adventerprisek9-m.ssa.high_iron_20200929` (Switch)

## Configure Ubuntu Server

The `arping` command is required for this lab, but its not included in the base Ubuntu server image. To install it, we must first provide internet connectivity to the server.

This can be done by using Pnetlab `cloud_nat` network feature.

<img src="/lan-switching/.images/1.png" width="300">

Connect the server to the `cloud_nat` node and then install the tool from the terminal.

<img src="/lan-switching/.images/2.png" width="700">

If you'are done, you can remove the `cloud_nat`. Turn on the switch (viosl2) and run these commands:

```bash
switch> enable
switch# show interfaces status
switch# show mac address-table
```

The output should look similar to this:

<img src="/lan-switching/.images/3.png" width="600">

As you can see, the switch does not have any connected devices, and its `MAC address table` is empty.

## Building the topology

Now, let's build this simple topology in pnetlab:

<img src="/lan-switching/.images/4.png" width="500">

<img src="/lan-switching/.images/5.png" width="500">

We can to see the new entries in the MAC address table.

<img src="/lan-switching/.images/6.png" width="700">

## Some Useful Commands

```bash
# Displays a one-line summary for all interfaces.
show interfaces status 

# Shows all dynamically learned MAC addresses in the switch's MAC table.
show mac address-table dynamic

# Searches the MAC table for a specific dynamic MAC address.
show mac address-table dynamic address <some_mac_address>

# Shows all dynamic MAC addresses learned within a specific interface.
show mac address-table dynamic interface Gi0/0

# Shows all dynamic MAC addresses learned on a specific interface VLAN.
show mac address-table dynamic vlan 1

# Displays detailed information for a specific interface.
show interfaces Gi0/0

# Shows detailed error counters for a specific interface (often empty on virtual switches).
show interfaces Gi0/0 counters

# Displays a summary of packet and byte counters (Pkts In, Pkts Out) for a specific interface.
show interfaces Gi0/0 stats
```

## Send Ethernet Frames

From the Linux instance, you can use this command to send ethernet frame to switch.

```bash
arping -I eth0 -S 0.0.0.0 -c 1 0.0.0.0
```

Command breakdown:

- `arping`: A linux tool that sends Layer 2 ARP packets directly onto the local network.
- `-I eth0`: This flag specifies which `network interface` to send the packet from. In this case, `eth0`.
- `-S 0.0.0.0`: This is the most importatnt part. It sets the `source IP address` inside the ARP packet to `0.0.0.0`.
    - Normally, `arping` would use the interfaces real IP.
    - Using `0.0.0.0` (which means "unspecified" or "no address") signals that this is an `"ARP Probe"`. The device is not yet caliming an IP, it's just asking about one.
- `-c 1`: This tells `arping` to send only 1 packet and then stop.
- `0.0.0.0`: this is the `destination IP` that the ARP packet is asking about.
    - The command is asking, "Who has the IP address 0.0.0.0?".
    - When a device frist joins a network and has no IP, it sends ARP probe for its own intended IP. But in this specific command, its probing for 0.0.0.0 itself, which is a special case sometimes used during the initial DAD (Duplicate Address Detection) process.

First, check the current packet counters on the switch Gi0/0 interface:

<img src="/lan-switching/.images/7.png" width="700">

Note that the `Pkts In` (Packets In) counter is currently 163.

Next, lets send 3 Ethernet frames from the Linux host to the switch using the `arping` command:

<img src="/lan-switching/.images/8.png" width="700">

This command transmits 3 packets. Now, lets check the switch interface counters again:

<img src="/lan-switching/.images/9.png" width="700">

As you can see, the `Pkts In` counter has increased from 163 to 166. This confirms that the switch received the 3 frames sent from the host.

## Aging and Clearing

You can view the switch default `aging time` and the current number of entries in the MAC address table using the following commands.

```bash
# MAC address table aging parameters
show mac address-table aging-time

# Number of MAC addresses in the table
show mac address-table count
```

<img src="/lan-switching/.images/10.png" width="700">

You can manually remove entries from the MAC address table.

```bash
# Clears ALL dynamic MAC addresses from the table
clear mac address-table dynamic

# Clears dynamic entries for a specific VLAN only
clear mac address-table dynamic vlan <vlan-number>

# Clears dynamic entries learned on a specific interface
clear mac address-table dynamic interface <interface-id>

# Clears a single dynamic entry by specifying its MAC address
clear mac address-table dynamic address <mac-address>
```

## MAC Address Tables with Multiple Switches

This scenario demonstrates how MAC address learning and forwarding decisions operate independently on each switch. When hosts communicate across the network, both switches learn the source MAC addresses of all devices.

The key, however, is which port they learn them on.


<img src="/lan-switching/.images/11.png" width="700">

Switch1 MAC table shows two types of entries: 
- **Locally Learned**: It has learned the MAC addresses for Fred (...0200) and Barney (...0300) on their respective access ports, Gi0/0 and Gi0/1.
- **Remotely Learned**: It has learned the MAC addresses for all hosts on Switch2 (Wilma, Betty, and the host ...f5e7) on a single port: Gi0/2. This is because, from Switch1's perspective, any frame originating from those remote hosts must arrive through the inter-switch link connected to Gi0/2.

<img src="/lan-switching/.images/12.png" width="700">

Switch2's MAC table shows the exact opposite:

- **Locally Learned**: It has learned the MAC addresses for Wilma (...0700), Betty (...0400), and the host ...f5e7 on their specific access ports: Gi0/0, Gi0/3, and Gi1/0.

- **Remotely Learned**: It has learned the MAC addresses for both Fred (...0200) and Barney (...0300) on port Gi0/2. This port is its only path to reach Switch1.

<img src="/lan-switching/.images/13.png" width="700">

This demonstrates the core logic of a switch: it doesn't know the full network topology, it only knows **which port to use to reach a specific MAC address**.
