# DHCP Relay & Client Lab

This lab demonstrates how to implement a **Centralized DHCP Server** architecture. Instead of deploying a DHCP server at every branch office, we use a central router at HQ to manage IP pools for remote locations.

This configuration requires **DHCP Relay** (`ip helper-address`), allowing broadcast DHCP requests to traverse the WAN link as unicast packets.

## Network Topology

* **R1-HQ (Server):** Central Router hosting the DHCP service and internet simulation.
* **R2-Branch (Relay):** Gateway for the branch LAN. Intercepts DHCP broadcasts.
* **SW1-Branch (Client):** Layer 2 switch obtaining its management IP dynamically.
* **Linux-Host (Client):** End-user workstation.

<img src="/chapter-19/.images/09.png">

## Addressing Plan

| Device | Interface | IP Address | Subnet Mask | Role |
| :--- | :--- | :--- | :--- | :--- |
| **R1-HQ** | `Gi0/0` | `10.0.0.1` | `255.255.255.252` | DHCP Server / WAN |
| **R2-Branch** | `Gi0/0` | `10.0.0.2` | `255.255.255.252` | WAN Link |
| **R2-Branch** | `Gi0/1` | `192.168.10.1` | `255.255.255.0` | Gateway / Relay Agent |
| **SW1-Branch** | `vlan 1` | **DHCP** | `255.255.255.0` | DHCP Client |
| **Linux-1** | `eth0` | **DHCP** | `255.255.255.0` | DHCP Client |

---

## Configuration

### 1. Centralized DHCP Server (R1-HQ)

R1 acts as the server. It requires a **Static Route** to the remote branch network. Without this, R1 could assign an IP, but it wouldn't know how to send the "DHCPOFFER" packet back to the Relay Agent.

```sh
# 1. EXCLUDE STATIC IPS (Gateway & Reserved)
ip dhcp excluded-address 192.168.10.1 192.168.10.9
    
# 2. DEFINE DHCP POOL FOR REMOTE SUBNET
ip dhcp pool BRANCH_LAN
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
 exit

# 3. INTERFACE CONFIGURATION
int g1
 description WAN Link to Branch
 ip address 10.0.0.1 255.255.255.252
 no shutdown
 exit
   
# 4. ROUTING (CRITICAL)
# Route traffic for the branch LAN back via R2
ip route 192.168.10.0 255.255.255.0 10.0.0.2

show ip dhcp excluded-address all
show ip dhcp pool
```

<img src="/chapter-19/.images/04.png">

<img src="/chapter-19/.images/05.png">
    
### 2. DHCP Relay Agent (R2-Branch)

R2 sits between the clients and the server. The `ip helper-address` command 
is applied to the **LAN interface** (where the broadcasts arrive), not the WAN interface.

```sh
int g0/0
 description WAN Link to HQ
 ip address 10.0.0.2 255.255.255.252
 no shutdown
 exit

int g0/1
 description LAN Gateway for Branch Users
 ip address 192.168.10.1 255.255.255.0
 # FORWARD DHCP BROADCASTS TO HQ SERVER
 ip helper-address 10.0.0.1
 no shutdown
 exit
```

### 3. Switch DHCP Client (SW1-Branch)

The switch is configured to obtain its management IP automatically via the SVI 
(Switch Virtual Interface).

```sh
# 1. ACCESS PORTS CONFIGURATION
int range g0/0-2
 description Connected to End Users
 switchport mode access
 switchport access vlan 1
 no shutdown
 exit

# 2. MANAGEMENT INTERFACE (SVI)
int vlan 1
 description Management IP via DHCP
 # The switch will request an IP from the Relay Agent (R2)
 ip address dhcp
 no shutdown
 exit
```
    
## Verification

### 1. Verify DHCP Pool Status (R1-HQ)

Check active leases on the server. We expect to see the Switch and the Linux host.

```sh
show ip dhcp binding
```

<img src="/chapter-19/.images/03.png">

### 2. Verify Relay Configuration (R2-Branch)

Confirm the helper address is set on the correct interface.

```sh
show ip int g0/1
```

<img src="/chapter-19/.images/01.png">

### 3. Verify Client Lease (SW1-Branch)

Check the negotiated IP, Subnet Mask, and Lease Timer.

```sh
show dhcp lease
```

<img src="/chapter-19/.images/02.png">

### 4. End-to-End Connectivity

1.  DHCP provided the correct IP and Gateway.

<img src="/chapter-19/.images/07.png">

2.  Linux 1 and 2 is correctly routing traffic to SW-Branch and R1-HQ.

<img src="/chapter-19/.images/08.png">

<img src="/chapter-19/.images/06.png">
