# OSPF

This schema extension contains all you need to model the OSPF Routing Protocol.

Dependencies: `base, extensions.routing`

## Overview

- **Version:** 1.0

## Nodes

### OSPF

- **Description:** OSPF (Open Shortest Path First) instance on a Virtual Router.
- **Label:** OSPF
- **Icon:** mdi:network-outline
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**router_id__address__value, vrf__name__value, device__name__value
- **Uniqueness Constraints:**device + vrf + version__value

#### Attributes

| name | kind | optional | default_value | description | order_weight | choices |
| ---- | ---- | -------- | ------------- | ----------- | ------------ | ------- |
| reference\_bandwidth | Number | True | 1000 | Reference bandwidth for OSPF instance \(in Mbps\)\. | 1150 | \`\` |
| version | Dropdown |  | ospf | Version of the OSPF protocol\. | 1100 | \`ospf, ospfv3\` |
| import\_policies | Text | True |  |  | 1300 | \`\` |
| export\_policies | Text | True |  |  | 1350 | \`\` |

#### Relationships

| name | peer | optional | cardinality | kind | label | identifier |
| ---- | ---- | -------- | ----------- | ---- | ----- | ---------- |
| router\_id | IpamIPAddress | True | one | Attribute |  |  |
| ospf\_interfaces | RoutingOSPFInterface | True | many | Component | OSPF Interfaces | ospf\_\_ospfinterfaces |

### OSPFInterface

- **Description:** Pivot table linking OSPF configuration to an interface.
- **Label:** OSPF Interface
- **Icon:** mdi:ethernet
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**description__value
- **Uniqueness Constraints:**ospf + interface

#### Attributes

| name | kind | optional | description | order_weight | choices | default_value |
| ---- | ---- | -------- | ----------- | ------------ | ------- | ------------- |
| description | Text | False | Description of the OSPF interface\. | 1500 | \`\` |  |
| metric | Number | True | OSPF metric for the interface\. | 1400 | \`\` |  |
| mode | Dropdown |  | Mode of the OSPF interface\. | 1300 | \`normal, passive, peer\_to\_peer\` | normal |
| authentication\_key | Password | True | Shared secret used to authenticate and secure routing messages between neighboring routers\. | 1250 | \`\` |  |
| authentication\_mode | Dropdown | True |  | 1225 | \`md5, sha1\` |  |
| area | Text |  | OSPF area associated with the interface\. | 1200 | \`\` |  |

#### Relationships

| name | label | peer | identifier | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | ---------- | -------- | ----------- | ---- | ------------ |
| ospf | OSPF | RoutingOSPF | ospf\_\_ospfinterfaces | False | one | Parent | 1100 |
| interface |  | DcimInterfaceL3 |  | False | one | Attribute | 1200 |
