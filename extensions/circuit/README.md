# Circuit

This schema extension contains Circuits and ways to connect them with your infrastructure! The circuit could be a fiber connecting two sites, you would then have two endpoints, one on each site.


Dependencies: `base, extentions.location_minimal`
## Overview
- **Version:** 1.0
## Nodes
### **Circuit**
- **Description:** A Circuit represent service operated by a provider.
- **Label:** Circuit
- **Icon:** mdi:cable-data
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** circuit_id__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | unique | optional | description | choices |
| ---- | ---- | ------ | -------- | ----------- | ------- |
| circuit_id | Text | True |  |  |  |
| description | Text |  | True |  |  |
| circuit_type | Dropdown |  |  | Specifies the type of circuit. | [{'name': 'upstream', 'label': 'Upstream', 'description': 'Connection to an upstream provider or Internet service provider (ISP)', 'color': '#1e90ff'}, {'name': 'peering', 'label': 'Peering', 'description': 'Connection to another network for exchange of traffic', 'color': '#20b2aa'}, {'name': 'dark_fiber', 'label': 'Dark Fiber', 'description': 'Leased, unlit fiber for customer management and operation', 'color': '#333333'}, {'name': 'mpls', 'label': 'MPLS', 'description': 'Multi-Protocol Label Switching circuit for QoS-based routing', 'color': '#7f00ff'}] |
| status | Dropdown |  |  |  | [{'name': 'active', 'label': 'Active', 'description': 'Fully operational and currently in service.', 'color': '#7fbf7f'}, {'name': 'provisioning', 'label': 'Provisioning', 'description': 'In the process of being set up and configured.', 'color': '#ffff7f'}, {'name': 'maintenance', 'label': 'Maintenance', 'description': 'Undergoing routine maintenance or repairs.', 'color': '#ffd27f'}, {'name': 'drained', 'label': 'Drained', 'description': 'Temporarily taken out of service.', 'color': '#bfbfbf'}] |

#### Relationships
| name | peer | optional | cardinality | kind | label | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ----- | ------------ |
| provider | OrganizationProvider | False | one | Attribute |  |  |
| location | LocationHosting | True | one | Attribute | Location | 1500 |
| enpoints | DcimCircuitEndpoint | True | many | Component |  |  |

### **CircuitEndpoint**
- **Description:** A circuit endpoint, could be a position in a MMR...
- **Label:** Circuit Endpoint
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimCircuit
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** circuit + name__value
---
#### Attributes
| name | kind | description | order_weight | optional | choices |
| ---- | ---- | ----------- | ------------ | -------- | ------- |
| name | Text | Name of the circuit endoint, could be a MMR position for instance. | 1000 |  |  |
| status | Dropdown |  |  | True | [{'name': 'active', 'label': 'Active', 'description': 'Fully operational and currently in service.', 'color': '#7fbf7f'}, {'name': 'provisioning', 'label': 'Provisioning', 'description': 'In the process of being set up and configured.', 'color': '#ffff7f'}, {'name': 'maintenance', 'label': 'Maintenance', 'description': 'Undergoing routine maintenance or repairs.', 'color': '#ffd27f'}, {'name': 'drained', 'label': 'Drained', 'description': 'Temporarily taken out of service.', 'color': '#bfbfbf'}] |
| description | Text |  |  | True |  |

#### Relationships
| name | peer | order_weight | optional | cardinality | kind | label |
| ---- | ---- | ------------ | -------- | ----------- | ---- | ----- |
| circuit | DcimCircuit | 900 | False | one | Parent |  |
| location | LocationHosting | 1500 | False | one | Attribute | Location |

## Extensions
### OrganizationProvider
#### Attributes
|  |
|  |

#### Relationships
| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| circuits | DcimCircuit | many | True |

### LocationHosting
#### Attributes
|  |
|  |

#### Relationships
| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| circuits | DcimCircuit | many | True |
