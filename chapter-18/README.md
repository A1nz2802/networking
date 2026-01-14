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
