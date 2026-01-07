# IPv4 Addressing

This chapter covers the following topics:

- Perspectives on IPv4 Subnetting
- Analyzing Classful IPv4 Networks
- Analyzing Subnet Masks
- Analyzing Existing Subnets
- Subnet Design

## 1. Binary Fundamentals & Power of 2

Core reference table. Memorizing powers of 2 (up to $2^{16}$) is mandatory for rapid mental subnetting and binary conversion.

<img src="/chapter-11-15/.images/01.png" height="450">

## 2. RFC 1918: Private Address Space

Reserved ranges for internal networks not routable on the public internet.

<img src="/chapter-11-15/.images/03.png">

## 3. Classful Network Reference

Although we use Classless (CIDR) routing today, the **Default Mask** is the starting point for all subnetting questions.

<img src="/chapter-11-15/.images/02.png">

>[!Note]
The address range of all addresses that begin with `0` and `127` are reserved.
Visit **IANA IPv4 special-purpose address registry** for more details.

## 4. The Magic Number Strategy
This is the key to solving problems mentally. The "Interesting Octet" is the octet where the mask is neither 0 nor 255.

<img src="/chapter-11-15/.images/04.png">

>[!IMPORTANT]
**Key Rule:** The value of the lowest "on" bit in the mask is your Magic Number.

## 5. Examples: Analyzing Subnets

### Scenario A: Analyzing a CIDR Block

- **Input:** `IP Address` + `/Prefix`
- **Focus:** Indetity the "Interesting Octet" directly from the prefix length.

<img src="/chapter-11-15/.images/05.png">

1. Identity the Class (A, B or C) to determine the **Default Mask**.
2. Locate the **Interesting Octet** (when the prefix ends).
3. Calculate **Active Bits** in that octet (`Current Prefix` - `Previous Octet Boundary`).
4. Use the **LSB Value Method** (Powers of 2) to find the **Magic Number**.

### Scenario B: Analyzing a Decimal Mask

- **Input:** `IP Address` + `Subnet Mask`
- **Foucs:** Convert the mask to CIDR first to simplify the mental process.

<img src="/chapter-11-15/.images/06.png">

1. Convert the Decimal Mask to CIDR.
2. Calculate the **Magic Number** by substracting the interesting octet value from 256.
3. Find the **Subnet ID** by finding the multiple of the Magic Number closest to (but not greater than) the IP's value in that octet.
