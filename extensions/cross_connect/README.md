# Cross Connect

This extension contains schema to capture Cross Connect. You can see it as "a cable operated by a provider". You will be able to attach it to a location and then connect endpoints to it (e.g. rear interface of a patch panel, circuit endpoint ...)


Dependencies: `base`
## Overview
- **Version:** 1.0
## Nodes
### **CrossConnect**
- **Description:** Cross-connect between different endpoints within a datacenter.
- **Label:** Cross-Connect
- **Icon:** streamline:arrow-crossover-right-solid
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** provider__name__value
- **Uniqueness Constraints:** provider + identifier__value
---
#### Attributes
| name | kind | order_weight | optional | choices |
| ---- | ---- | ------------ | -------- | ------- |
| identifier | Text | 900 |  |  |
| description | Text | 1300 | True |  |
| status | Dropdown | 1200 | True | [{'name': 'connected', 'label': 'Connected', 'description': 'Fully operational and currently in connected', 'color': '#7fbf7f'}, {'name': 'planned', 'label': 'Planned', 'description': 'In the process of being set up', 'color': '#ffff7f'}, {'name': 'reserved', 'label': 'Reserved', 'description': 'Fully connected and reserved for a future use', 'color': '#9090de'}] |

#### Relationships
| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| location | Location | LocationHosting | False | one | Attribute | 1100 |
| provider |  | OrganizationProvider | False | one | Attribute | 1000 |
