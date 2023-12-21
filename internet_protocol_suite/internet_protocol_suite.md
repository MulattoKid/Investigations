# Internet Protocol Suite

## Intro
The internet protocol suite provides a model for how end-to-end data communcation should be packetized, addressed, transmitted, routed and received. The suite is split into four layers: 1) application layer, 2) transport layer, 3) internet layer and 4) link layer.

## IP Address
The IP address is a 32- or 128-bit address that identifies computers in a network. The IP address of computers on a local network need to be distinct, but can have the same values as computers on a different local network. The IP address of computers that are connected to public networks need to have an IP address assigned from a restricted pool, so that no two computers have the same IP address.

E.g. pinging *google.com* shows that it's IP address is `142.250.74.142`. This is what a domain is, it's a unique text version of an IP address, and it's the *DNS* server's job of resolving domains to IP addresses.

At home, each of your network devices does most likely not have individual public IP addresses. Instead, it's the router that's directly connected to your internet service provider that has a public IP, while all devices connected to it are given "private" IP addresses, e.g. `192.168.10.2`. The router also has a private IP address on the local network it creates, e.g. `192.168.10.1`.

### Ports

## MAC Address
Unlike IP addresses, MAC addresses are tied to each network component, and cannot change. I.e. your router, laptop, phone, TV all have a MAC address that uniquely identifies them. So, MAC addresses work on the link (physical) layer, and are e.g. used in the Ethernet protocol.

When sending an ethernet frame, the source and destination MAC addresses are required. However, it's important to note that the destination MAC address
isn't the MAC address of the final receiver, but rather the MAC address of the next receiver in the chain. It is the IP address that denotes the final receiver. So, when sending data from A -> B -> C -> D, the IP address of D will always be used as the destination address in the internet layer, whereas the destination MAC address will change for each transfer.

## References
- https://www.youtube.com/watch?v=3b_TAYtzuho
- https://youtu.be/aamG4-tH_m8?si=w0XLV8n7hYPhxEWR
