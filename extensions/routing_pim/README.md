# PIM

This schema extension contains all you need to model the PIM Protocol.

Dependencies: `base, extensions.routing`

## Overview

- **Version:** 1.0

## Nodes

### PIM

- **Description:** Protocol Independent Multicast (PIM) instance on a Virtual Router.
- **Label:** PIM
- **Icon:** mdi:network-outline
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** vrf__name__value, device__name__value
- **Uniqueness Constraints:** device + vrf
#### Attributes

| name | kind | optional | default_value | description | order_weight |
| ---- | ---- | -------- | ------------- | ----------- | ------------ |
| dr_priority | Number | True | 1 | Designated Router priority. | 1250 |
| import_policies | Text | True |  |  | 1300 |
| export_policies | Text | True |  |  | 1350 |

#### Relationships

| name | peer | optional | description | cardinality | kind | label | identifier |
| ---- | ---- | -------- | ----------- | ----------- | ---- | ----- | ---------- |
| rp_address | IpamIPAddress | True | Rendezvous Point (RP) address for PIM. | one | Attribute |  |  |
| pim_interfaces | RoutingPIMInterface | True |  | many | Component | PIM Interfaces | pim__piminterfaces |

### PIMInterface

- **Description:** Interface configuration for PIM.
- **Label:** PIM Interface
- **Icon:** mdi:ethernet
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** description__value
- **Uniqueness Constraints:** pim + interface
#### Attributes

| name | kind | optional | description | order_weight | choices | default_value |
| ---- | ---- | -------- | ----------- | ------------ | ------- | ------------- |
| description | Text | False | Description of the OSPF interface. | 1100 | `` |  |
| pim_mode | Dropdown |  | PIM mode used for multicast routing on this interface. | 1150 | `sparse, dense, bidirectional` |  |
| hello_interval | Number | True | Interval for PIM hello messages (in seconds). | 1300 | `` | 30 |
| dr_priority | Number | True | Designated Router priority on the interface. | 1250 | `` | 1 |

#### Relationships

| name | label | peer | identifier | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | ---------- | -------- | ----------- | ---- | ------------ |
| pim | PIM | RoutingPIM | pim__piminterfaces | False | one | Parent |  |
| interface |  | DcimInterfaceL3 |  | False | one | Attribute | 1200 |
