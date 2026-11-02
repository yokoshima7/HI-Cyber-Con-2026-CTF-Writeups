# Ghost in the Wire (Forensics)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=618323b5-0af7-493c-b35c-7c61c3dc7a0f) · Agentic AI division

The supplied ZIP has SHA-256 `392084661bebf2a86f4194056436ddb2b78917577bc259cc07e1210f007c563c`. Its PCAP contains 30 Ethernet/IPv4/ICMP frames. Four frames from `192.168.1.100` to `10.0.0.5` are ordinary noise. The other 26 are echo requests from `10.13.37.1` to `10.13.37.2`, numbered 1 through 26.

Filter to that source, destination, and ICMP echo request type (`icmp.type == 8`). Sort by ICMP sequence number and read the one-byte payload of each request. The 26 bytes concatenate to:

```text
hiCTF{1cmp_3xf1l_d3t3ct3d}
```

The sequence numbers provide the ordering, so packet capture order is not an assumption. The team's final public solved list includes Ghost in the Wire; the flag text above comes directly from the filtered payloads.
