## OSPF Terminology Glossary

| Term | Description |
| :--- | :--- |
| **Routing Protocol** | A set of messages, rules, and algorithms used by routers for the overall purpose of learning routes (e.g., RIP, EIGRP, OSPF). |
| **Routed Protocol** | A protocol that defines packets that can be routed/forwarded by a router (e.g., IPv4, IPv6). |
| **Convergence** | The process where all routers collectively realize something has changed, advertise the changes, and choose the currently best routes. |
| **IGP (Interior Gateway Protocol)** | A routing protocol designed and intended for use inside a single Autonomous System (AS). |
| **EGP (Exterior Gateway Protocol)** | A routing protocol designed for use between different Autonomous Systems (e.g., BGP). |
| **Autonomous System (AS)** | A network under the administrative control of a single organization. |
| **Link-State Algorithm** | A routing algorithm where routers build a full map of the network topology (LSDB) before calculating routes. |
| **Metric (Cost)** | The value OSPF uses to choose the best route, calculated as the sum of interface costs along the path (based on bandwidth). |
| **LSA (Link-State Advertisement)** | A data structure with specific information about the network topology, stored inside the LSDB. |
| **LSDB (Link-State Database)** | The collection of all LSAs known to a router; identical on all routers in an area. |
| **Flooding** | The process of forwarding LSAs to all other routers so that every router has the same information. |
| **SPF (Shortest Path First)** | The Dijkstra algorithm used by routers to process the LSDB and calculate the best routes to add to the IP routing table. |
| **Router ID (RID)** | A 32-bit number (usually a dotted-decimal number like an IP) that uniquely identifies an OSPF router. |
| **Hello Message** | A packet sent to discover neighbors, supply parameters, and act as a keepalive mechanism. |
| **Hello Interval** | The regular time interval at which a router sends Hello messages. |
| **Dead Interval** | The time a router waits without receiving a Hello before assuming the neighbor has failed (default is 4x Hello Interval). |
| **2-Way State** | A neighbor state where the router has received a Hello from the neighbor containing its own RID; stable state for DROthers. |
| **Full State** | A neighbor state where routers have fully exchanged their LSDB contents. |
| **LSU (Link-State Update)** | The OSPF packet used to send LSAs to neighbors. |
| **DR (Designated Router)** | The elected router on a broadcast network (Ethernet) that manages the database exchange to improve efficiency. |
| **BDR (Backup Designated Router)** | The router that takes over the DR role if the current DR fails. |
| **DROther** | A router on a broadcast segment that is neither the DR nor the BDR. |
| **Adjacency (Fully Adjacent)** | A relationship between neighbors that have reached the Full state and synchronized their LSDBs. |
| **Single-Area OSPF** | An OSPF design where all interfaces on all routers are assigned to the same area (usually Area 0). |
| **Area** | A grouping of routers and links that share detailed LSDB info, reducing SPF workload for the entire network. |
| **ABR (Area Border Router)** | An OSPF router with interfaces connected to the backbone area and at least one other area. |
| **Backbone Area** | A special OSPF area (Area 0) to which all other areas must connect. |
| **Router LSA (Type 1)** | An LSA created by every router to describe itself, its interfaces, and its state within an area. |
| **Network LSA (Type 2)** | An LSA created by the DR to describe a subnet and the routers connected to it. |
| **Summary LSA (Type 3)** | An LSA created by an ABR to describe a subnet located in another area. |
