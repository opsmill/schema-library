# VLAN Translation

This schema extension is based on Juniper VLAN MAP, and not yet test out for other vendors.


Dependencies: `base.dcim`
## Overview
- **Version:** 1.0
## Nodes
### **MapInOut**
- **Description:** VLAN Mapping for In/Out operations
- **Label:** VLAN Map In/Out
- **Icon:** ph:swap
- **Menu Placement:** DcimInterface
- **Include in Menu:** ✅

#### Ordering and Constraints
- **Order By:** interface__name__value, direction__value, operation__value
- **Uniqueness Constraints:** interface + direction__value
---
#### Attributes
| name | kind | description | label | order_weight | choices | optional |
| ---- | ---- | ----------- | ----- | ------------ | ------- | -------- |
| direction | Dropdown | Direction of the mapping | Map Direction | 1050 | [{'name': 'input', 'label': 'Input', 'description': 'Input direction', 'color': '#D2B4DE'}, {'name': 'output', 'label': 'Output', 'description': 'Output direction', 'color': '#A9CCE3'}] | True |
| operation | Dropdown | Operation type | Map Operation | 1100 | [{'name': 'pop', 'label': 'POP', 'description': 'Single POP operation', 'color': '#B2D4E6'}, {'name': 'pop_pop', 'label': 'POP-POP', 'description': 'Double POP operation', 'color': '#AED6F1'}, {'name': 'pop_swap', 'label': 'POP-SWAP', 'description': 'POP then SWAP operation', 'color': '#A9DFBF'}, {'name': 'push', 'label': 'PUSH', 'description': 'Single PUSH operation', 'color': '#CDEACC'}, {'name': 'push_push', 'label': 'PUSH-PUSH', 'description': 'Double PUSH operation', 'color': '#9FA8DA'}, {'name': 'swap', 'label': 'SWAP', 'description': 'Single SWAP operation', 'color': '#D2B4DE'}, {'name': 'swap_push', 'label': 'SWAP-PUSH', 'description': 'SWAP then PUSH operation', 'color': '#C4B7E6'}, {'name': 'swap_swap', 'label': 'SWAP-SWAP', 'description': 'Double SWAP operation', 'color': '#CBC3E3'}] | True |
| vlan_id_swap | Number | VLAN ID to swap to during SWAP operations | VLAN ID Swap | 1200 |  | True |
| inner_vlan_id | Number | Inner VLAN ID for operations involving double VLAN tags | Inner VLAN ID | 1300 |  | True |
| inner_tag_protocol_id | Number | Inner tag protocol ID (TPID) | Inner Tag Protocol ID | 1400 |  | True |
| tag_protocol_id | Number | Tag protocol ID (TPID) for outer VLAN operations | Tag Protocol ID | 1500 |  | True |

#### Relationships
| name | kind | peer | description | cardinality | optional | label | order_weight |
| ---- | ---- | ---- | ----------- | ----------- | -------- | ----- | ------------ |
| interface | Parent | DcimInterface | Interface to which the Input/Output VLAN mapping is applied | one | False | Interface | 1000 |

## Extensions
### DcimInterface
#### Relationships
| name | kind | peer | description | cardinality | label | order_weight |
| ---- | ---- | ---- | ----------- | ----------- | ----- | ------------ |
| network_maps | Component | NetworkMapInOut | Interface Input/Output VLAN mapping | many | Input/Output MAP | 1600 |
