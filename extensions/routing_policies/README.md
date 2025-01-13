# Routing Policies

This schema extension contains a generic to create Routing Policies.

This Generic can be extend for each Routing Protocols you may want to use.



Dependencies: `base`
## Overview
- **Version:** 1.0
## Generics
### **Policy**
- **Description:** Policy defining the rules for routing traffic in a network.
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value
---
#### Attributes
| name | kind | description | unique | optional | order_weight | label | choices | default_value |
| ---- | ---- | ----------- | ------ | -------- | ------------ | ----- | ------- | ------------- |
| name | Text | The name of the routing policy. | True | False | 1000 |  |  |  |
| description | Text | An optional description of the routing policy. |  | True | 1100 |  |  |  |
| policy_type | Dropdown | The type of routing policy which specifies the direction of route advertisement. |  |  | 1200 | Type | [{'name': 'import-policy', 'label': 'Import', 'description': 'Policy for incoming routes.', 'color': '#E6E6FA'}, {'name': 'export-policy', 'label': 'Export', 'description': 'Policy for outgoing routes.', 'color': '#E6E6FA'}, {'name': 'import-export-policy', 'label': 'Import + Export', 'description': 'Policy for both incoming and outgoing routes.', 'color': '#E6E6FA'}] |  |
| weight | Number | Priority of the routing policy. The higher the number, the higher the priority. |  | True | 1400 |  |  | 1000 |
| address_family | Dropdown | The address family for the routing policy indicating the type of IP address. |  |  | 1150 |  | [{'name': 'ipv4', 'label': 'IPv4', 'description': 'Policy applies to IPv4 addresses.', 'color': '#E6E6FA'}, {'name': 'ipv6', 'label': 'IPv6', 'description': 'Policy applies to IPv6 addresses.', 'color': '#E6E6FA'}, {'name': 'all', 'label': 'All', 'description': 'Policy applies to both IPv4 and IPv6 addresses.', 'color': '#E6E6FA'}] | all |
