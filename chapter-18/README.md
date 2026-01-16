# Labs in this chapter:

- [Router-on-a-Stick (ROAS) Lab](#router-on-a-stick-roas-lab)
- [Layer 3 Switching with SVIs Lab](#layer-3-switching-with-svis-lab)
- [Layer 3 EtherChannel Lab](#layer-3-etherchannel-lab)

# Router-on-a-Stick (ROAS) Lab

This lab demonstrates **Inter-VLAN Routing** using a "Router-on-a-Stick" topology. It connects isolated VLANs using a single physical router interface divided into virtual subinterfaces (802.1Q Trunking).

## Network Topology

Logical topology showing the single physical link (Stick) carrying tagged traffic for VLANs 10, 20, and untagged traffic for Native VLAN 99.

<img src="/chapter-18/.images/05.png">

## Addressing Plan

| Device | Interface | VLAN ID | IP Address | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Router B1** | `g1.10` | 10 | `10.1.10.1/24` | Gateway for Sales |
| **Router B1** | `g1.20` | 20 | `10.1.20.1/24` | Gateway for Engineering |
| **Router B1** | `g1.99` | 99 | `10.1.99.1/24` | Native VLAN (Mgmt) |
| **Linux 1** | `eth0` | 10 | `10.1.10.10/24` | Host in Sales |
| **Linux 2** | `eth0` | 20 | `10.1.20.10/24` | Host in Engineering |

---

## Device Configuration

### 1. Switch SW1 (Layer 2)

Trunk configuration on `g0/0` (facing router) and access ports `g0/1` & `g0/2` (facing hosts).

```sh
conf t
! Create VLAN Database
vlan 10
 name Sales
vlan 20
 name Engineering
vlan 99
 name Native_Mgmt
exit

! Trunk Configuration (facing Router B1)
int g0/0
 description Trunk to Router
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 no shutdown
 exit

! Access Ports
int g0/1
 description Host Linux 1
 switchport mode access
 switchport access vlan 10
 no shutdown

int g0/2
 description Host Linux 2
 switchport mode access
 switchport access vlan 20
 no shutdown
```

### 2. Router B1 (The "Stick")
Configuration of subinterfaces with 802.1Q encapsulation.

```sh
conf t
! Physical Interface
int g1
 no ip address
 no shutdown
 exit

! Subinterface for VLAN 10
int g1.10
 encapsulation dot1q 10
 ip address 10.1.10.1 255.255.255.0
 exit

! Subinterface for VLAN 20
int g1.20
 encapsulation dot1q 20
 ip address 10.1.20.1 255.255.255.0
 exit

! Native VLAN Configuration (Security)
int g1.99
 encapsulation dot1q 99 native
 ip address 10.1.99.1 255.255.255.0
 exit
```

### 3. Linux Hosts Configuration

Temporary IP configuration using `iproute2` commands.

```sh
# on Linux 1 (VLAN 10)
ip addr add 10.1.10.10/24 dev eth0
ip link set eth0 up
ip route add default via 10.1.10.1

# on Linux 2 (VLAN 20)
ip addr add 10.1.20.10/24 dev eth0
ip link set eth0 up
ip route add default via 10.1.20.1
```

## Verification

### 1. Layer 2 Trunk Status (Switch)

Verify that g0/0 is trunking, Native VLAN is 99, and correct VLANs are allowed.

```sh
SW1# show interfaces status
SW1# show vlan brief
```

<img src="/chapter-18/.images/01.png">
<br>
<img src="/chapter-18/.images/02.png">

### 2. ROAS Status (Router)

Verify that subnets are "Directly Connected" via subinterfaces `g1.10` and `g1.20`.

```sh
RouterB1# show ip interface brief
RouterB1# show ip route
```

<img src="/chapter-18/.images/03.png">

The `show vlans` command confirms that the router is processing tagged traffic.

```sh
RouterB1# show vlans
```

<img src="/chapter-18/.images/04.png">

### 3. End-to-End Connectivity (Ping)

Test Inter-VLAN routing by pinging from Linux 1 to Linux 2.

```sh
# ping to Linux 2
root@linux1:~# ping -c 4 10.1.20.10

# ping to VLAN 10 Gateway
root@linux1:~# ping -c 2 10.1.10.1

# ping to VLAN 20 Gateway
root@linux1:~# ping -c 6 10.1.20.1
```

# Layer 3 Switching with SVIs Lab

This lab demonstrates **Inter-VLAN Routing** performed directly on a Multilayer Switch using **Switched Virtual Interfaces (SVIs)**. Unlike the previous ROAS topology, the router is offloaded from local routing duties, significantly improving network performance.

The Switch acts as the Default Gateway for the end devices.

## Network Topology

Logical topology showing the Layer 3 Switch containing the gateways (SVIs) and the uplink to Router B1 via a transit VLAN.

<img src="/chapter-18/.images/21.png">

## Addressing Plan

| Device | Interface | VLAN | IP Address | Role |
| :--- | :--- | :--- | :--- | :--- |
| **SW1 (L3 Switch)** | `vlan 10` | 10 | `10.1.10.1/24` | Gateway for Sales |
| **SW1 (L3 Switch)** | `vlan 20` | 20 | `10.1.20.1/24` | Gateway for Engineering |
| **SW1 (L3 Switch)** | `vlan 30` | 30 | `10.1.30.1/24` | Link to Router |
| **Router B1** | `g1` | - | `10.1.30.2/24` | WAN Uplink |
| **Linux 1** | `eth0` | 10 | `10.1.10.10/24` | Host |
| **Linux 2** | `eth0` | 20 | `10.1.20.10/24` | Host |

---

## Device Configuration

### 1. Enabling Layer 3 Routing (SW1)
The most critical step is enabling the routing engine on the switch hardware.

```bash
SW1(config)# ip routing
```

### 2. SVI Configuration (SW1)

Instead of physical subinterfaces, we configure logical VLAN interfaces.

```sh
interface vlan 10
 ip address 10.1.10.1 255.255.255.0
 no shutdown

interface vlan 20
 ip address 10.1.20.1 255.255.255.0
 no shutdown

interface vlan 30
 ip address 10.1.30.1 255.255.255.0
 no shutdown
```

<img src="/chapter-18/.images/20.png">

### 3. Physical Port Assignment (Layer 2)

For an SVI to be in the `up/up` state, the VLAN must have at least one 
active physical port assigned to it. Additionally, the uplink to the router 
is configured as a standard Access port (VLAN 30), as the router is unaware of VLAN tags.

```sh
! Uplink Port to Router (Access Mode)
int e0/0
 description Link to Router B1
 switchport mode access
 switchport access vlan 30
 no shutdown
 exit

! Access Ports for Linux Hosts
int e0/1
 description Linux 1 - VLAN 10
 switchport mode access
 switchport access vlan 10
 no shutdown
 exit

int e0/2
 description Linux 2 - VLAN 20
 switchport mode access
 switchport access vlan 20
 no shutdown
 exit
```

### 4. Return Route (Router B1)

Since the external Router is not directly connected to VLAN 10 or 20, it requires a 
static route pointing to the Switch SVI to return traffic.

```sh
ip route 10.1.0.0 255.255.0.0 10.1.30.1
```

### 5. Linux Hosts Configuration

The Gateway is now the Switch SVI, NOT the Router.

```sh
# on Linux 1 Host (VLAN 10)
ip addr add 10.1.10.10/24 dev eth0
ip link set eth0 up
ip route add default via 10.1.10.1

# on Linux 2 Host (VLAN 20)
ip addr add 10.1.20.10/24 dev eth0
ip link set eth0 up
ip route add default via 10.1.20.1
```

## Verification

### 1. Route Verification (Switch)

Verify that the switch has populated its routing table with "Connected" routes for the VLANs.

```sh
show ip route connected
```

<img src="/chapter-18/.images/22.png">

### 2. SVI Status Check

Ensure that the VLAN interfaces are in up/up state. 
Note that an SVI is only "up" if at least one port in that VLAN is active.

```sh
show ip interface brief | include Vlan
```

<img src="/chapter-18/.images/23.png">

### 3. Internal Connectivity Test

Test routing between VLAN 10 and VLAN 20. 
This traffic stays inside the switch.

From Linux 1: ping 10.1.20.10

```sh
# on Linux 1 ping to Linux 2
ping 10.1.20.10
```

### 4. Uplink Connectivity Test

Test routing from a VLAN to the external Router B1. 
This verifies the transit VLAN 30.

```sh
# on Linux 1 ping to Router B1
ping 10.1.30.2
```

# Layer 3 EtherChannel Lab

This lab demonstrates how to aggregate multiple physical links into a single logical 
**Routed Interface** (Layer 3 EtherChannel).

Unlike Layer 2 EtherChannels, this configuration **removes Spanning Tree Protocol (STP)** 
from the equation entirely. The link acts as a single point-to-point connection with an IP 
address, providing **high bandwidth** and immediate **failover redundancy**.

## Network Topology

Two Layer 3 Switches connected via **3 physical cables** bundled into one logical **Port-Channel**.

<img src="/chapter-18/.images/30.png">

## Addressing Plan

| Device | Interface | IP Address | Subnet Mask | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Switch 1** | `Port-channel 1` | `10.0.0.1` | `255.255.255.252` | L3 Core Link |
| **Switch 1** | `vlan 10` | `192.168.10.1` | `255.255.255.0` | Gateway (Sales) |
| **Switch 2** | `Port-channel 1` | `10.0.0.2` | `255.255.255.252` | L3 Core Link |
| **Switch 2** | `vlan 20` | `192.168.20.1` | `255.255.255.0` | Gateway (HR) |
| **Linux 1** | `eth0` | `192.168.10.10` | `255.255.255.0` | Host |
| **Linux 2** | `eth0` | `192.168.20.10` | `255.255.255.0` | Host |

---

## Configuration

### 1. Converting to Layer 3 Ports

The most distinctive step in this lab is the use of the `no switchport` command. 
This converts the interface from a switch port (dealing with MACs/VLANs) to a routed 
port (dealing with IPs).

```sh
# On SW1 and SW2
interface range g0/0-2
 no switchport
 channel-group 1 mode active
```

### 2. Configuring the Logical Interface

We assign the IP address to the bundle (Port-channel), not the physical cables.

```sh
# On SW1 and SW2
interface port-channel 1
 no switchport
 ip address 10.0.0.1 255.255.255.252
```

### 3. Routing Logic

Since the switches are routing traffic, they need to know how to reach the 
remote networks. We use Static Routes for simplicity.

```sh
# SW1 (route to right side)
ip route 192.168.20.0 255.255.255.0 10.0.0.2

# SW2 (route to lef side)
ip route 192.168.10.0 255.255.255.0 10.0.0.1
```

### 4. Linux Hosts Configuration

Configuring the IP and pointing the Default Gateway to the local Switch VLAN Interface.

```sh
# On Linux 1
ip addr add 192.168.10.10/24 dev eth0
ip link set eth0 up
ip route add default via 192.168.10.1

# On Linux 2
ip addr add 192.168.20.10/24 dev eth0
ip link set eth0 up
ip route add default via 192.168.20.1
```

## Verification

### 1. Verify EtherChannel Status

Check if the bundle is active and which protocol is being used (LACP). Look for the **"RU"** flags.
* **R** = Layer 3 (Routed)
* **U** = In Use (Up)

```sh
show etherchannel summary
```

<img src="/chapter-18/.images/31.png">

### 2. Verify Routing Table

Ensure the static routes are loaded and point to the Port-channel interface.

```sh
show ip route
```

<img src="/chapter-18/.images/32.png">

### 3. End-to-End Connectivity

Perform a ping from Linux 1 to Linux 2. The traffic will flow through the EtherChannel.

```sh
# On Linux 1
ping 192.168.20.10
```

<img src="/chapter-18/.images/33.png">

### 4. Redundancy Test (Chaos Engineering)

Start a continuous ping, then disconnect one or two cables (e.g., Delete link `g0/1`). 
The ping should continue with minimal interruption.

```sh
ping 192.168.20.10
```

<img src="/chapter-18/.images/34.png">
