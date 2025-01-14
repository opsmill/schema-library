# Routing Policies OSPF

This extension is using the Routing Policies extensions and the Routing OSPF one together.


Dependencies: `base, extensions.routing, extensions.routing_policies, extensions.routing_ospf`
## Overview
- **Version:** 1.0
## Nodes
### **PolicyOSPF**
- **Description:** A routing policiers for OSPF
- **Label:** OSPF Routing Policies
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌
---
## Extensions
### RoutingOSPF
#### Attributes
| name | kind | state |
| ---- | ---- | ----- |
| import_policies | Text | absent |
| export_policies | Text | absent |

#### Relationships
| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import_routing_policies | Import Routing Policies | RoutingPolicyOSPF | ospf__import_policies | The routing-policies used by this instance for import. | Generic | many |
| export_routing_policies | Export Routing Policies | RoutingPolicyOSPF | ospf__export_policies | The routing-policies used by this instance for export. | Generic | many |
