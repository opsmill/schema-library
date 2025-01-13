# Routing Policies (PIM)

This schema inherits the `RoutingPolicy` schema and removes `import_policies` and `export_policies` attributes. However it adds a number of relatopnships to `RoutingPIM`.


Dependencies: `base, extensions.routing, extensions.routing_policies, extensions.routing_pim`
## Overview
- **Version:** 1.0
## Nodes
### **PolicyPIM**
- **Description:** A routing policiers for PIM
- **Label:** PIM Routing Policies
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌
---
## Extensions
### RoutingPIM
#### Attributes
| name | kind | state |
| ---- | ---- | ----- |
| import_policies | Text | absent |
| export_policies | Text | absent |

#### Relationships
| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import_routing_policies | Import Routing Policies | RoutingPolicyPIM | pim__import_policies | The routing-policies used by this instance for import. | Generic | many |
| export_routing_policies | Export Routing Policies | RoutingPolicyPIM | pim__export_policies | The routing-policies used by this instance for export. | Generic | many |
