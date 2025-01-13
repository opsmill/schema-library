# VRRP

This schema extension contains models for VRRP.


Dependencies: `base, base.dcim, base.ipam`
## Overview
- **Version:** 1.0
## Nodes
### **VRRPGroup**
- **Description:** VRRP Group configuration
- **Label:** VRRP Group
- **Icon:** fluent:virtual-network-20-filled
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value
---
#### Attributes
| name | kind | label | unique | description | order_weight | optional |
| ---- | ---- | ----- | ------ | ----------- | ------------ | -------- |
| name | Text | Name | True | Unique name of the entry | 1000 |  |
| group | Text | Group |  | VRRP Group | 1100 |  |
| password | HashedPassword | Password |  | VRRP Password/Key | 1400 | True |

#### Relationships
| name | on_delete | description | label | peer | optional | cardinality | kind | order_weight |
| ---- | --------- | ----------- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| ip_address | cascade | VRRP IP (v4 or v6) | IP Address | IpamIPAddress | True | many | Attribute | 1200 |
| vrrp_interfaces | cascade |  | VRRP Interfaces | NetworkVRRPInterface |  | many | Component | 1300 |

### **VRRPInterface**
- **Description:** VRRP Interface configuration
- **Label:** VRRP Interface
- **Icon:** carbon:interface-usage
- **Menu Placement:** NetworkVRRPGroup
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** priority__value
- **Uniqueness Constraints:** vrrp_group + interface
---
#### Attributes
| name | kind | label | description | regex | default_value | order_weight |
| ---- | ---- | ----- | ----------- | ----- | ------------- | ------------ |
| priority | Number | VRRP Priority | VRRP Priority (Should be between 0 to 255) | ^(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])$ | 100 | 1100 |

#### Relationships
| name | description | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----------- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| vrrp_group | VRRP Group | VRRP Group | NetworkVRRPGroup | False | one | Attribute | 1200 |
| interface | Interface L3 | Interface | DcimInterfaceL3 | False | one | Attribute | 1300 |

## Extensions
### DcimInterfaceL3
#### Relationships
| name | kind | peer | description | cardinality | label | order_weight |
| ---- | ---- | ---- | ----------- | ----------- | ----- | ------------ |
| vrrp | Component | NetworkVRRPInterface | VRRP Interface Configuration | one | VRRP | 1500 |

### IpamIPAddress
#### Relationships
| name | kind | peer | description | cardinality | label | order_weight |
| ---- | ---- | ---- | ----------- | ----------- | ----- | ------------ |
| vrrp | Component | NetworkVRRPGroup | Part of VRRP Group | one | VRRP Group | 1600 |
