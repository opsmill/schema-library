# OSPF

This schema extension contains all you need to model the OSPF Routing Protocol.


Dependencies: `base, extensions.routing`
## Overview
- **Version:** 1.0
## Nodes
### **OSPF**
- **Description:** OSPF (Open Shortest Path First) instance on a Virtual Router.
- **Label:** OSPF
- **Icon:** mdi:network-outline
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** router_id__address__value, vrf__name__value, device__name__value
- **Uniqueness Constraints:** device + vrf + version__value
---
#### Attributes
| name | kind | optional | default_value | description | order_weight | choices |
| ---- | ---- | -------- | ------------- | ----------- | ------------ | ------- |
| reference_bandwidth | Number | True | 1000 | Reference bandwidth for OSPF instance (in Mbps). | 1150 |  |
| version | Dropdown |  | ospf | Version of the OSPF protocol. | 1100 | [{'name': 'ospf', 'label': 'OSPFv2', 'description': 'Open Shortest Path First version 2.', 'color': '#E6E6FA'}, {'name': 'ospfv3', 'label': 'OSPFv3', 'description': 'Open Shortest Path First version 3.', 'color': '#E6E6FA'}] |
| import_policies | Text | True |  |  | 1300 |  |
| export_policies | Text | True |  |  | 1350 |  |

#### Relationships
| name | peer | optional | cardinality | kind | label | identifier |
| ---- | ---- | -------- | ----------- | ---- | ----- | ---------- |
| router_id | IpamIPAddress | True | one | Attribute |  |  |
| ospf_interfaces | RoutingOSPFInterface | True | many | Component | OSPF Interfaces | ospf__ospfinterfaces |

### **OSPFInterface**
- **Description:** Pivot table linking OSPF configuration to an interface.
- **Label:** OSPF Interface
- **Icon:** mdi:ethernet
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** description__value
- **Uniqueness Constraints:** ospf + interface
---
#### Attributes
| name | kind | optional | description | order_weight | choices | default_value |
| ---- | ---- | -------- | ----------- | ------------ | ------- | ------------- |
| description | Text | False | Description of the OSPF interface. | 1500 |  |  |
| metric | Number | True | OSPF metric for the interface. | 1400 |  |  |
| mode | Dropdown |  | Mode of the OSPF interface. | 1300 | [{'name': 'normal', 'label': 'Normal', 'description': 'Standard OSPF interface mode.', 'color': '#E6E6FA'}, {'name': 'passive', 'label': 'Passive', 'description': 'Interface will not send OSPF hello packets.', 'color': '#E6E6FA'}, {'name': 'peer_to_peer', 'label': 'Peer-to-Peer', 'description': 'OSPF peer-to-peer interface mode.', 'color': '#E6E6FA'}] | normal |
| authentication_key | Password | True | Shared secret used to authenticate and secure routing messages between neighboring routers. | 1250 |  |  |
| authentication_mode | Dropdown | True |  | 1225 | [{'name': 'md5', 'label': 'MD5', 'color': '#E6E6FA'}, {'name': 'sha1', 'label': 'SHA1', 'color': '#E6E6FA'}] |  |
| area | Text |  | OSPF area associated with the interface. | 1200 |  |  |

#### Relationships
| name | label | peer | identifier | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | ---------- | -------- | ----------- | ---- | ------------ |
| ospf | OSPF | RoutingOSPF | ospf__ospfinterfaces | False | one | Parent | 1100 |
| interface |  | DcimInterfaceL3 |  | False | one | Attribute | 1200 |
