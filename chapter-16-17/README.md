## Network Topology

This lab simulates a simple enterprise network with a central router (Router A) connecting to two remote branches (Router B and Router C) via point-to-point WAN links.

<img src="/chapter-16-17/.images/02.png">

## Subnetting Plan

| Segment Name | Network Address | CIDR | Type | Interface Assignment Plan |
| :--- | :--- | :--- | :--- | :--- |
| **LAN A** | `172.16.1.0` | `/24` | LAN | Router A: `.1` / Hosts: `.2 - .254` |
| **LAN B** | `172.16.2.0` | `/24` | LAN | Router B: `.1` / Hosts: `.2 - .254` |
| **LAN C** | `172.16.3.0` | `/24` | LAN | Router C: `.1` / Hosts: `.2 - .254` |
| **WAN A** | `172.16.10.0` | `/24` | P2P Link | Router A (Gi2): `.1` / Router B (Gi0/0): `.2` |
| **WAN B** | `172.16.11.0` | `/24` | P2P Link | Router A (Gi3): `.1` / Router C (Gi0/0): `.2` |

## Host Configuration (Ubuntu Server)

Open the configuration file: 

```sh
nano /etc/netplan/01-netcfg.yaml
```

Define static IP and gateway.

```yml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 172.16.1.2/24
      routes:
        - to: 0.0.0.0/0
          via: 172.16.1.1
      nameservers:
        addresses:
          - 8.8.8.8
```

```sh
# for Host B
172.16.2.2/24
172.16.2.1 

# for Host C
172.16.3.2/24
172.16.3.1
```

Generate the backend configuration and apply it.

```sh
# Generate config for networkd
netplan generate
# Apply the config
netplan apply
```

Verify IP assignment and routing table.

```sh
# Check IP address
ip a

# Check routing table
ip r

# Check DNS resolutioon
resolvectl dns
```

## Router Configuration

### Router A Config

Router A requires specific routes to reach the remote LANs (LAN B and LAN C).

```sh
RouterA# configure terminal

RouterA(config)# int g1
RouterA(config-if)# description Link to LAN A
RouterA(config-if)# ip address 172.16.1.1 255.255.255.0
RouterA(config-if)# no shutdown

RouterA(config)# int g2
RouterA(config-if)# description Link to Router B (WAN A)
RouterA(config-if)# ip address 172.16.10.1 255.255.255.0
RouterA(config-if)# no shutdown
RouterA(config-if)# exit

RouterA(config)# int g3
RouterA(config-if)# description Link to Router C (WAN B)
RouterA(config-if)# ip address 172.16.11.1 255.255.255.0
RouterA(config-if)# no shutdown
RouterA(config-if)# exit

RouterA# show  ip interface brief
```

<img src="/chapter-16-17/.images/03.png">

**Static Routing Configuration**: Define paths to remote networks using the next-hop IP addresses.

```sh
# Static Network Routes
RouterA(config)# ip route 172.16.2.0 255.255.255.0 172.16.10.2
RouterA(config)# ip route 172.16.3.0 255.255.255.0 172.16.11.2

RouterA# show ip route static
RouterA# show running-config | include ip route
```

<img src="/chapter-16-17/.images/04.png">

⚠️ While Cisco IOS allows configuring static routes
using the exit interface (e.g., `ip route 172.16.2.0 255.255.255.0 g2`), 
this is discouraged on Ethernet links. Using the exit interface on a multi-access 
network (like Ethernet) forces the router to send ARP requests for every destination 
IP, relying on the neighbor's **Proxy ARP** feature to reply. 
This causes:

- High ARP traffic overhead.
- A bloated ARP table (one entry per destination host instead of one per router).

**Always use the Next-Hop IP address** for static routes over Ethernet to ensure 
efficient Layer 2 resolution.

### Router B Config

Router B acts as a stub network. A default route is used to send all non-local 
traffic to Router A.

```sh
RouterB(config)# int g0/1
RouterB(config-if)# description Link to LAN B
RouterB(config-if)# ip address 172.16.2.1 255.255.255.0
RouterB(config-if)# no shutdown

RouterB(config)# ing g0/0
RouterB(config-if)# description Link to Router A (WAN A)
RouterB(config-if)# ip address 172.16.10.2 255.255.255.0
RouterB(config-if)# no shutdown

RouterB# show ip interface brief
```

**Static Routing Configuration**: Configure a Gateway of Last Resort pointing to Router A.

```sh
RouberB(config)# ip router 0.0.0.0 0.0.0.0 172.16.10.1
```

### Router C Config

Similar to Router B, Router C uses a default route to reach the rest of the network.

```bash
RouterC# configure terminal
RoterC(config)# int g0/1
RoterC(config-if)# desciption Link to LAN C 
RoterC(config-if)# ip address 172.16.3.1 255.255.255.0
RoterC(config-if)# no shutdown

RouterC(config)# int g0/0
RouterC(config-if)# description Link to Router A (WAN B)
RouterC(config-if)# ip address 172.16.11.2 255.255.255.0
RouterC(config-if)# no shutdown

RouterC(config)# ip route 0.0.0.0 0.0.0.0 172.16.11.1
```

### Verification

Verify static routes (network and default)

<img src="/chapter-16-17/.images/06.png">

From A, ping to B and C

<img src="/chapter-16-17/.images/05.png">

## Static Host Routes and Floating Static Routes

###  Topology Changes

Add a new connecion on Router B to Router C.

<img src="/chapter-16-17/.images/07.png">

```sh
RouterB(config)# interface g0/2
RouterB(config-if)# description Link to Router C (Backup Path)
RouterB(config-if)# ip address 172.16.20.1 255.255.255.0
RouterB(config-if)# no shutdown
```

```sh
RouterC(config)# interface g0/2
RouterC(config-if)# description Link to Router B (Transit)
RouterC(config-if)# ip address 172.16.20.2 255.255.255.0
RouterC(config-if)# no shutdown
```

```sh
# Route traffic for LAN B via the Transit Link
RouterC(config)# ip route 172.16.2.0 255.255.255.0 172.16.20.1

# Floating Default Route (Return path backup)
# if the link to A fails, return traffic goes via C.
RouterB(config)# ip route 0.0.0.0 0.0.0.0 172.16.20.2 50
```

### Static Host Route (Traffic Engineering)

We want traffic destined for the specific server Host B (`172.16.2.2`) to 
take the longer path via Router C, while the rest of LAN B traffic uses the direct link (A->C->B). 

```sh
# /32 mask enforces a "Longest Prefix Match", taking precedence over the /24 route.
RouterA(config)# ip route 172.16.2.2 255.255.255.255 172.16.11.2
```

### Floating Static Route (Redundancy)

If the primary link (WAN A) fails, traffic to LAN B should automatically failover to the path via Router C.

```sh
# this route stays hidden in the configuration until the primary route fails.
RouterA(config)# ip route 172.16.2.0 255.255.255.0 172.16.11.2 50
```

### Verification

Visualizing Traffic Paths (Host Route) from Host A, compare the path 
to the general LAN B vs. the specific Server B.
- **Target:** `172.16.2.1` (Router B) --> should take the direct path (1 hop).
- **Target:** `172.16.2.2` (Host B) --> should take the detour via Router C (3 hops).

```sh
# Verify General Path
traceroute 172.16.2.1

# Verify Host Route Path
traceroute 172.16.2.2
```

<img src="/chapter-16-17/.images/08.png">

Simulate a failure by shutting down the primary WAN link on Router A.

```sh
RouterA(config)# interface g2
RouterA(config-if)# shutdown
```

<img src="/chapter-16-17/.images/09.png">

<img src="/chapter-16-17/.images/10.png">

## Optional: Internet Access Setup (NAT)

To install tools like `traceroute` on the Ubuntu Host, the network requires internet access via Router A.

- Connect Router A (Gi4) to the Cloud/NAT node.
- Configure Interface and NAT on Router A:

```sh
RouterA(config)# interface GigabitEthernet4
RouterA(config-if)# ip address dhcp
RouterA(config-if)# ip nat outside
RouterA(config-if)# no shutdown
RouterA(config-if)# exit
```
