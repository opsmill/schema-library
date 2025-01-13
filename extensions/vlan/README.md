# VLAN

This schema extension contains models to support VLANs in you network.


Dependencies: `base`
## Overview
- **Version:** 1.0
## Nodes
### **VLAN**
- **Description:** A VLAN is isolated layer two domain
- **Label:** VLAN
- **Icon:** mdi:lan-pending
- **Menu Placement:** IpamL2Domain
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** l2domain + vlan_id__value
---
#### Attributes
| name | kind | optional | choices |
| ---- | ---- | -------- | ------- |
| name | Text |  |  |
| description | Text | True |  |
| vlan_id | Number |  |  |
| status | Dropdown |  | [{'name': 'active', 'label': 'Active', 'description': 'Fully operational and currently in service.', 'color': '#7fbf7f'}, {'name': 'provisioning', 'label': 'Provisioning', 'description': 'In the process of being set up and configured.', 'color': '#ffff7f'}, {'name': 'maintenance', 'label': 'Maintenance', 'description': 'Undergoing routine maintenance or repairs.', 'color': '#ffd27f'}, {'name': 'drained', 'label': 'Drained', 'description': 'Temporarily taken out of service.', 'color': '#bfbfbf'}] |
| role | Dropdown | True | [{'name': 'server', 'label': 'Server', 'description': 'Dedicated systems for managing networked resources.', 'color': '#c4bed7'}, {'name': 'management', 'label': 'Management', 'description': 'Network segments for administrative and control tasks.', 'color': '#9af1e1'}, {'name': 'user', 'label': 'User', 'description': 'Segments designed for end-user access and activities.', 'color': '#a0b78d'}] |

#### Relationships
| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| location | LocationHosting | True | many |  |  |
| prefixes | IpamPrefix | True | many |  |  |
| l2domain | IpamL2Domain | False | one | Attribute | 1200 |

### **L2Domain**
- **Description:** Represents layer 2 domain.
- **Label:** Layer 2 Domain
- **Icon:** mdi:domain-switch
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | order_weight |
| ---- | ---- | ------------ |
| name | Text | 1000 |

#### Relationships
| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| vlans | IpamVLAN | True | many | Component |

## Extensions
### IpamPrefix
#### Relationships
| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| vlan | IpamVLAN | True | one | Attribute | 1400 |

### DcimInterfaceL2
#### Relationships
| name | label | peer | optional | cardinality | kind | identifier |
| ---- | ----- | ---- | -------- | ----------- | ---- | ---------- |
| untagged_vlan | Untagged VLAN | IpamVLAN | True | one | Component | interface_l2__untagged_vlan |
| tagged_vlan | Tagged VLANs | IpamVLAN | True | many | Component | interface_l2__tagged_vlan |

### LocationHosting
#### Relationships
| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| vlans | VLANs | IpamVLAN | many | True |
