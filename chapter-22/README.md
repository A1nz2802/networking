# OSPFv2 Single-Area Configuration Lab

This lab demonstrates how to implement a basic **OSPFv2 Single-Area** network architecture (Area 0). After an OSPF design has been chosen, the configuration can be as simple as enabling OSPF on each router interface and placing that interface in the correct OSPF area.

This configuration utilizes the traditional OSPFv2 `network` command along with wildcard masks to indirectly enable the OSPF process on specific interfaces. Loopback interfaces are also configured to simulate internal LANs and provide a stable Router ID.

## Network Topology

* **R1, R2, R3:** Routers participating in the OSPF Area 0 backbone.
* **SW1:** Central switch creating a broadcast multi-access network (`192.168.1.0/24`), which will trigger a DR/BDR election.
* **Loopbacks (lo0):** Emulate isolated remote subnets (`/32`) and establish the OSPF `router-id` for each device.

<img src="/chapter-22/.images/01.png">

## Addressing Plan

| Device | Interface | IP Address | Subnet Mask / Wildcard | Role |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | `Gi0/0` | `192.168.1.1` | `255.255.255.0` | OSPF Area 0 Link |
| **R1** | `lo0` | `1.1.1.1` | `255.255.255.255` | Router ID / Simulated LAN |
| **R2** | `Gi0/0` | `192.168.1.2` | `255.255.255.0` | OSPF Area 0 Link |
| **R2** | `lo0` | `2.2.2.2` | `255.255.255.255` | Router ID / Simulated LAN |
| **R3** | `Gi0/0` | `192.168.1.3` | `255.255.255.0` | OSPF Area 0 Link |
| **R3** | `lo0` | `3.3.3.3` | `255.255.255.255` | Router ID / Simulated LAN |

---

## Configuration

### 1. Enabling OSPF on Router 1 (R1)

- Uses the `router ospf process-id` global command to enter OSPF configuration mode. 
- Configures the OSPF router ID explicitly. Step 3 uses the `network` command with a wildcard mask to enable OSPFv2 on matched interfaces.

```sh
# 1. INITIALIZE OSPF PROCESS
router ospf 1

# 2. SET THE ROUTER ID MANUALLY
 router-id 1.1.1.1

# 3. ENABLE OSPF ON SPECIFIC INTERFACES
 # Matches Gi0/0 (192.168.1.1)
 network 192.168.1.0 0.0.0.255 area 0
 
 # Matches Loopback 0 (1.1.1.1)
 network 1.1.1.1 0.0.0.0 area 0
 exit
```

```sh
# on R2
router ospf 1
 router-id 2.2.2.2
 network 192.168.1.0 0.0.0.255 area 0
 network 2.2.2.2 0.0.0.0 area 0
 exit
```

```sh
# on R3
router ospf 1
 router-id 3.3.3.3
 network 192.168.1.0 0.0.0.255 area 0
 network 3.3.3.3 0.0.0.0 area 0
 exit
```

## Verification

### 1. Verify OSPF Neighbor Adjacencies

Check the neighbor table to confirm routers have successfully 
formed adjacencies and observe the DR/BDR election results on the broadcast segment.

```sh
show ip ospf neighbor
```

<img src="/chapter-22/.images/02.png">

### 2. Verify the OSPF Routing Table

Confirm that R1 has learned the remote loopback networks (`2.2.2.2/32` and `3.3.3.3/32`) dynamically via OSPF. These routes will be marked with an "O".

```sh
show ip route ospf
```

<img src="/chapter-22/.images/03.png">

### 3. Check the Link-State Database (LSDB)

Inspect the LSDB to view the exact LSA types generated in the area.
In a single-area design, you will primarily see **Router Link States** (Type 1) and **Net Link States** (Type 2).

```
show ip ospf database
```

<img src="/chapter-22/.images/04.png">

### 4. Verify Active OSPF Interfaces

Get a brief summary of all interfaces currently participating in the OSPF process, 
their assigned Area, and their current State (DR, BDR, DROTHER, or LOOPBACK).

```
show ip ospf interface brief
```

<img src="/chapter-22/.images/05.png">

### 5. Check Hello/Dead Timers and Interface Cost

Verify the exact OSPF parameters operating on a specific physical link. 
This output confirms the interface cost used for the SPF calculation and 
the Hello/Dead intervals (default is 10/40 on Ethernet).

```sh
show ip ospf interface g0/0
```

<img src="/chapter-22/.images/06.png">

### 6. Check Reference Bandwidth and Backbone Information

Display global OSPF process statistics. This confirms the current **Router ID**, 
the number of **interfaces** in Area 0, the number of times the **SPF algorithm** has 
been executed, and the default **reference bandwidth**.

```sh
show ip ospf
```

<img src="/chapter-22/.images/07.png">

### 7. Check the States DD/LSU

Use debugging to watch the OSPF adjacency process in real-time. By flapping the 
interface, we can observe the **DR/BDR election**, **Master/Slave negotiation** (EXSTART), 
**DBD packet exchange** (EXCHANGE), and **LSA requests/updates** (LOADING to FULL).

```sh
# on R1
# 1. Enable OSPF Adjacency Debugging on R1
debug ip ospf adj

# 2. Flap the interface to force a new election
configure terminal
int g0/0
 shutdown
 no shutdown

# 3. Stop debugging once the state reaches FULL
undebug all
```

<img src="/chapter-22/.images/08.png">

### 8. End-to-End Connectivity Test

Ensure that R1 can successfully reach the simulated LANs (Loopbacks) on the remote routers.

```sh
# Testing reachability from R1 to R3's loopback
ping 3.3.3.3
```

<img src="/chapter-22/.images/09.png">

## Advanced Troubleshooting & Manipulation

In this section, we intentionally manipulate OSPF parameters to observe how the protocol reacts to changes in priority, mismatched timers, and manual cost adjustments.

### Scenario 1: Forcing the DR/BDR Election (OSPF Priority)

**Objective:** By default, R3 (`3.3.3.3`) became the DR because it had the highest Router ID. We will manipulate the OSPF interface priority on R1 to force it to become the new Designated Router, despite having the lowest Router ID.

```sh
# 1. Check current roles (R3 is DR, R2 is BDR, R1 is DROTHER)
R1# show ip ospf neighbor

# 2. Change the OSPF priority on R1's interface (Default is 1, Max is 255)
R1# configure terminal
R1(config)# interface g0/0
R1(config-if)# ip ospf priority 255
R1(config-if)# end

# 3. OSPF does not preempt an existing DR. 
# We must reset the OSPF process on ALL routers to force a new election.
R1# clear ip ospf process
Reset ALL OSPF processes? [no]: yes

# (Execute 'clear ip ospf process' on R2 and R3 as well)
```

**Verification:** After the processes restart and adjacencies reach the `FULL` state, check the neighbor table on R2 or R3. R1 (`1.1.1.1`) will now be listed as the `DR`.

<img src="/chapter-22/.images/10.png">

### Scenario 2: Breaking Adjacencies (Mismatched Timers)

**Objective:** OSPF requires Hello and Dead timers to match exactly between neighbors to form an adjacency. We will change the Hello timer on R1 and observe the network fail.

```sh
# 1. Change the Hello interval on R1 to 5 seconds (Default is 10)
# Note: Changing the Hello timer automatically adjusts the Dead timer to 4x (20 sec)
R1# configure terminal
R1(config)# interface g0/0
R1(config-if)# ip ospf hello-interval 5
R1(config-if)# end

# 2. Wait for the original Dead timer (40 seconds) to expire on R2 and R3.
# You will see syslog messages indicating the neighbors have gone DOWN.
%OSPF-5-ADJCHG: Process 1, Nbr 2.2.2.2 on GigabitEthernet0/0 from FULL to DOWN, Neighbor Down: Dead timer expired

# 3. Verify that R1 has no OSPF neighbors
R1# show ip ospf neighbor
```

<img src="/chapter-22/.images/11.png">

**The Fix:** To restore the network, we must revert the timer on R1 back to the default, or configure R2 and R3 to match the new 5-second interval.

```sh
# Restore the default timer on R1
R1# configure terminal
R1(config)# interface g0/0
R1(config-if)# no ip ospf hello-interval
R1(config-if)# end
```


### Scenario 3: Traffic Engineering (Manipulating OSPF Cost)

**Objective:** OSPF uses Cost (derived from bandwidth) as its metric. The lowest total cost wins. We will manually configure a high cost on R1's interface to simulate a degraded or expensive link, forcing OSPF to update its routing metrics.

```sh
# 1. Check the baseline cost to reach R3's loopback (e.g., metric is 2)
R1# show ip route 3.3.3.3

# 2. Manually increase the OSPF cost of the physical interface
R1# configure terminal
R1(config)# interface g0/0
R1(config-if)# ip ospf cost 500
R1(config-if)# end

# 3. Verify the new routing table metric
R1# show ip route 3.3.3.3
```

**Verification:** You will notice that the metric in the routing table `[110/X]` has jumped significantly (e.g., to 501), reflecting the newly configured interface cost.

<img src="/chapter-22/.images/12.png">
