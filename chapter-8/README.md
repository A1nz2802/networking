# Implementing Ethernet Virtual LANs

This chapter covers the following topics:

- [VLAN Tagging Concepts](#vlan-tagging-concepts)
- [Creating VLANs and Assigning Access VLANs to an Interface](#creating-vlans-and-assigning-access-vlans-to-an-interface)
- [VLAN Trunking Protocol](#vlan-trunking-protocol)
- [VLAN Trunking Configuration](#vlan-trunking-configuration)
- [Implementing interfaces Connected to Phones](#implementing-interfaces-connected-to-phones)
- [Troubleshooting VLANs and VLAN Trunks](#troubleshooting-vlans-and-vlan-trunks)
- [Mismatched Native VLAN on a Trunk](#mismatched-native-vlan-on-a-trunk)

A LAN includes all devices in the same **broadcast domain**. A broadcast domain includes the set of all LAN-connected devices, so that when any of the devices sends a broadcast frame, all the other devices get a copy of the frame. So, from one perspective, you can think of a **LAN and a broadcast domain as being basically the same thing**.

When you are using VLANs in networks that have multiple interconnected switches, the switches need to use **VLAN trunking** on the links between the switches. VLAN trunking causes the switches to use a process called **VLAN tagging**, by which the sending switch adds another header to the frame before sending it over the **trunk**. This extra trunking header includes a **VLAN identifier (VLAN ID)** field so that the sending switch can associate the frame with a particular VLAN ID, and the receiving switch can then know in what VLAN each frame belongs.

## VLAN Tagging Concepts

 - Today, **802.1Q** has become the more popular trunking protocol, with Cisco not even bothering to support **ISL** in many of its switch models today.

- **802.1Q** inserts an extra 4-byte 802.1Q VLAN header into the original frame’s Ethernet header. In the 802.1Q header (12-bit), the VLAN ID field supports a theoretical maximun of 2^12 (4096) VLANs and 4094 in the practice.

<img src="/chapter-8/.images/01.png">

- Cisco switches break the range of VLAN IDs (1–4094) into two ranges: the **normal range** and the **extended range**. 

- 802.1Q also defines one special VLAN ID on each trunk as the **native VLAN** (defaulting to use VLAN 1).

## Creating VLANs and Assigning Access VLANs to an Interface

For a Cisco switch to forward frames in a particular VLAN, the switch must be configured to believe that the VLAN exists. In addition, the switch must have nontrunking interfaces (called `access interfaces` or `static access interfaces`) assigned to the VLAN and/or trunks that support the VLAN. The configuration steps for access interfaces are as follows:

- **Step 1:** To configure a new VLAN, follow these steps:
    - From configuration mode, use the `vlan vlan-id` command in global configuration mode to create the VLAN and to move the user into VLAN configuration mode.
        ```bash
        sw1(config)# vlan 2
        ```
    - (Optional) Use the `name <name>` command in VLAN configuration mode to list a name for the VLAN. If not configured, the VLAN name is 8 VLANZZZZ, where ZZZZ is the four-digit decimal VLAN ID.
        ```bash
        sw1(config-vlan)# name coolest vlan
        ```
- **Step 2:** For each access interface, follow these steps:
    - Use the `interface <type> <number>` command in global configuration mode to move into interface configuration mode for each desired interface.
        ```bash
        sw1(config)# int range g1/0-3
        ```
    - Use the switchport access vlan id-number command in interface configuration mode to specify the VLAN number associated with that interface.
        ```bash
        sw1(config-if-range)# switchport access vlan 2 
        ```
    - (Optional) Use the switchport mode access command in interface configuration mode to make this port always operate in access mode (that is, to not trunk).
        ```bash
        sw1(config-if-range)# switchport mode access
        sw1(config-if-range)# end

        sw1# show vlan brief
        ```
## VLAN Trunking Protocol

VLAN Trunking Protocol (**VTP**) is a Cisco proprietary tool on Cisco switches that advertises each VLAN configured in one switch so that all the other switches in the campus learn about that VLAN.

The current CCNA 200-301 exam blueprint ignores VTP, and many enterprise networks choose to disable it. For lab purposes, it is recommended to disable VTP to have full, local control over your switch configuration.

There are two primary modes used to effectively disable VTP:

- `vtp mode transparent`: This is the traditional method. In this mode, a switch does not participate in VTP (it won't learn or advertise VLANs) but it will forward VTP messages through its trunk links. It allows you to create and manage all VLANs (1-4094) locally, and the VLAN configuration is saved in the `running-config`.

- `vtp mode off`: This is a newer option on modern switches. It completely disables VTP. Like transparent mode, it allows local configuration of all VLANs and saves them in the `running-config`.

To check the current VTP status of your switch, use the `show vtp status` command.

>[!NOTE]
Do not change VTP settings on any switch that also connects to the production network until you know how VTP works.

## VLAN Trunking Configuration

In Cisco switches, the switchport `mode command` controls how an interface behaves.

- **The type of trunking**: IEEE 802.1Q, ISL, or negotiate which one to use, on switches
that support both types of trunking.
- **The administrative mode**: is the configuration you set, it's your intent (e.g., `access`, `trunk`, `dynamic desirable`, or `dynamic auto`)
- **The operational mode**: is the actual result, what the port is currently doing after negotiating with the device on the other end.

This negotiation uses a **Cisco proprietary protocol** called **DTP (Dynamic Trunking Protocol)**. The main thing to know is:

- `dynamic desirable`: actively tries to form a trunk.
- `dynamic auto`: passively waits to be asked to form a trunk.

The default mode is often `dynamic auto`, so if both switches are set to this, **a trunk will not form** because both are waiting passively. To form a trunk, you must set one side to `dynamic desirable ` or manually configure both sides as `trunk`.

<img src="/chapter-8/.images/02.png">

The `show interfaces trunk` command lists information about all interfaces that currenly operationally trunk; that is, lists interfaces that currently use VLAN trunking. With no interfaces listed, this command also confirms that the link between switches is not trunking.

For ports without the `switchport mode access` command—for instance, ports statically configured to trunk with the `switchport mode trunk` command—DTP still operates, but you can disable DTP negotiations altogether using the `switchport nonegotiate` interface subcommand.

## Implementing interfaces Connected to Phones

<img src="/chapter-8/.images/03.png">

**Step 1:** Use the `vlan <vlan-id>` command in global configuration mode to create the data and voice VLANs if they do not already exist on the switch.
```bash
# Check if VLAN 10 and 11 exists
sw1# show interfaces brief

# Create VLAN 10 and 11
sw1(config)# vlan 11
sw1(config)# vlan 10
```

**Step 2:** Configure the data VLAN like an access VLAN, as usual:

- Use the `interface <type> <number>` command in global configuration mode to move into interface configuration mode.
```bash
sw1(config)# int range f0/1-4
```
- Use the `switchport access vlan <id-number>` command in interface configuration mode to define the **data VLAN**.
```bash
sw1(config-if-range)# switchport access vlan 10
```
- Use the `switchport mode access` command in interface configuration mode to make this port always operate in access mode (that is, to not trunk).
```bash
sw1(config-if-range)# switchport mode access
```

**Step 3:** Use the `switchport voice vlan <id-number>` command in interface configuration mode to set the **voice VLAN ID**.
```bash
sw1(config-if-range)# switchport voice vlan 11
```

Verifying the status of a switch port configured.

```bash
sw1# show interfaces f0/4 switchport
```

<img src="/chapter-8/.images/04.png" width="500px">

## Troubleshooting VLANs and VLAN Trunks

Steps an engineer can take to avoid issues:

- **Step 1:** Confirm that the correct access VLANs have been assigned.
- **Step 2:** Confirm that all VLANs are both defined and active.
- **Step 3:** Check the allowed VLAN lists on both ends of each trunk to ensure that all VLANs intended to be used are included.
- **Step 4:** Check for incorrect trunk configuration settings that result in one switch operating as a trunk, with the neighboring switch not operating as a trunk.
- **Step 5:** Check the native VLAN settings on both ends of the trunk to ensure the
settings match.

To ensure that each access interface has been assigned to the correct VLAN, engineers need to confirm an interface operates as an access interface (as opposed to a **trunk interface**).

<img src="/chapter-8/.images/05.png">

First, on the issue of whether a VLAN exists on a switch, a VLAN can be defined to a switch in two ways: using the vlan number global configuration command, or it can be learned from another switch using VTP.

In addition to checking the configuration, you can check for the status of the VLAN (as well as whether it is known to the switch) using the show vlan command.

Shutting down a VLAN disables the VLAN on that switch only, so the switch will not forward frames in that VLAN.

Switch IOS gives you two similar configuration methods with which to disable (shutdown) and enable (no shutdown) a VLAN.

```bash
sw1(config)# no shutdown vlan 10
sw1(config)# shutdown vlan 20

sw1(config)# vlan 30
sw1(config-vlan)# no shutdown
sw1(config-vlan)# vlan 40
sw1(config-vlan)# shutdown
sw1(config-vlan)# end

sw1# show vlan brief
```

This image shows the incorrect configuration along with which side trunks and which does not. The side that trunks (SW1 in this case) enables trunking using the command **switch port mode trunk** but also disables Dynamic Trunking Protocol (DTP) negotiations using the switchport nonegotiate command. SW2’s configuration also helps create the problem, by using one of the two trunking options that rely on DTP. Because SW1 has disabled DTP, SW2’s DTP negotiations fail, and SW2 chooses to not trunk.

<img src="/chapter-8/.images/06.png">

## Mismatched Native VLAN on a Trunk

Unfortunately, it is possible to set the native VLAN ID to different VLANs on either end of the trunk, using the `switchport trunk native vlan <vlan-id>` command. If the native VLAN differ according to the two neighboring switches, the switches will cause frames sent in the native VLAN to jump from one VLAN to the other.

For example, if switch SW1 sends a frame using native VLAN 1 on an 802.1Q trunk, SW1 does not add a VLAN header, as is normal for the native VLAN. When switch SW2 receives the frame, noticing that no 802.1Q header exists, SW2 assumes that the frame is part of SW2’s configured native VLAN. If SW2 has been configured to think VLAN 2 is the native VLAN on that trunk, SW2 will try to forward the received frame into VLAN 2. (This effect of a frame being sent in one VLAN but then being believed to be in a different VLAN is called **VLAN hopping**.)
