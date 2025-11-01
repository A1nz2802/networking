# Configuring and Verifying Switch Interfaces

This chapter covering this topics:

- Autonegotiation Rules.
- [Configuring Speed, Duplex, and Description](#configuring-speed-duplex-and-description)

## Autonegotiation Rules:

**Case 1**: Autonegotiation enabled on both devices (Auto/Auto).

- **Process:** Both devices exchange their capabilities using Fast Link Pulses (FLPs).
- **Speed:** They agree to use the **highest common speed**.
- **Duplex:** They agree to use the **best common duplex** (Full-Duplex is always preferred).

**Case 2**: Autonegotiation enabled on one device (Auto). Disabled on the other (Manual).


- **Speed:** Detect the neighboring device’s physical layer standard by analyzing the
neighbor’s incoming frames. Use that speed.
- **Duplex:** The 'Auto' side **cannot detect duplex** and applies a default rule:
    - If speed is 10/100 Mbps **--->** defaults to **Half-Duplex**.
    - If speed is 1 Gbps or faster **--->** defaults to **Full-Duplex**.

`Parallel Detection`: A fallback mechanism used by an autonegotiation-enabled device when it does not receive any FLPs. It determines the link's speed by analyzing the partner's incoming electrical signal but cannot detect the duplex setting.

`Duplex Mistmatch`: A network fault state where one end of a link operates in full-duplex while the other end operates in half-duplex. This forces the half-duplex side (which must listen before sending, per CSMA/CD rules) to interpret simultaneous transmissions from the full-duplex side as "collisions." The result is a link that is technically "up" but has catastrophic performance due to constant errors and retransmissions.

>[!NOTE]
Never mix configurations. In real networks, use autonegotiation. If one side is set manually, the other side must be set to the exact same manual configuration.

>[!NOTE]
Hubs do not participate in autonegotiation, they do not generate FLP messages.

## Configuring Autonegotiation, Speed, and Duplex

### Use Autonegotiation on Cisco Switches

The commands `speed auto` and `duplex auto` are used to explicitly set an interface back to this default behavior. You can verify the results with `show interfaces status`, looking for the `a-` prefix (like `a-full` or `a-1000`) in the output, which confirms autonegotiation was successful.

```bash
sw1# configure terminal
sw1(config)# interface gigabitEthernet 0/0

sw1(config-if)# speed auto 
sw1(config-if)# duplex auto
sw1(config-if)# description Printer on 3rd floor, Preset to auto/autonegotiation-enabled

# Verify the operational status interfaces
sw1# show interfaces status
sw1# show interfaces g0/0

# Apply configuration to a range of interfaces
sw1(config)# interface range gigabitEthernet 0/0, 0/2
sw1(config-if-range)# description config for G0/0 AND G0/2 interfaces

sw1(config)# interface range gigabitEthernet 0/0-3
sw1(config-if-range)# description config for interfaces G0/0 through G0/3
```

### Setting Speed and Duplex Manually

Cisco recommends that you configure both devices on the ends of the link (to the same values, of course).

<img src="/chapter-7/.images/01.png">

`sw1` and `sw2` has default configuration.

>[!NOTE]
On some Cisco models, you must explicity disable autonegotiation whit `no negotiation auto` command before you can set the speed and duplex.

<img src="/chapter-7/.images/02.png" width="700">

```bash
sw1# configure terminal
sw1(config)# interface gigabitEthernet 0/0

# Disable autonegotiation
sw1(config-if)# no negotiation auto

# Set the speed and duplex
sw1(config-if)# speed 1000
sw1(config-if)# duplex full
sw1(config-if)# ^Z
sw1# show running-config interface gigabitEthernet 0/0
```

You can verifying manual configuration with `show running-config` or `show interfaces status` commands.

<img src="/chapter-7/.images/03.png" width="500">

<img src="/chapter-7/.images/04.png">
<img src="/chapter-7/.images/05.png">

As you can see, both `sw1` and `sw2` show the same operational settings (`full` and `1000`). The absence of the `a-` prefix on both switches confirms that autonegotiation is inactive and that the manual configuration has been correctly applied to both ends of the link.

## Using Auto-MDIX on Cisco Switches

`Auto-MDIX`, when enabled, gives an Ethernet interface the ability to sense when the attached cable uses the wrong cable pinout and to overcome the problem. For instance, a link between two switches should use a `crossover cable pinout`. If the cable has a `straight-through pinout`, the auto-MDIX feature can sense the issue and swap pairs in the interface electronics, achieving the same effect as a crossover cable.

- **Cisco Catalyst switches** use auto-MDIX by default, with a default interface subcommand of `mdix auto`.
- Auto-MDIX works if either one or both endpoints on the link enable auto-MDIX.
- To disable auto-MDIX, disable it on both ends of the link using the `no mdix auto` interface command.

```bash
sw1# configure terminal
sw1(config)# int g0/0
sw1(config-if)# no mdix auto
```

## Administratively Controlling Interface State with Shutdown

Cisco switches use the shutdown command to disable an interface and the no shutdown command to enable an interface.

```bash
sw1# configure terminal
sw1(config)# int g0/0
sw1(config-if)# shutdown
```

<img src="/chapter-7/.images/06.png">

To re-activate g0/0 interface, just use `no shutdown` command.

