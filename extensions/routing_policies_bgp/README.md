# Routing Policies BGP

This extension is using the Routing Policies extensions and the Routing BGP one together.


Dependencies: `base, extensions.routing, extensions.routing_policies, extensions.routing_bgp`
## Overview
- **Version:** 1.0
## Nodes
### **PolicyBGP**
- **Description:** A routing policiers for BGP
- **Label:** BGP Routing Policies
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌
---
## Extensions
### RoutingBGPPeerGroup
#### Attributes
| name | kind | state |
| ---- | ---- | ----- |
| import_policies | Text | absent |
| export_policies | Text | absent |

#### Relationships
| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import_routing_policies | Import Routing Policies | RoutingPolicyBGP | bgp__import_policies | The routing-policies used by this instance for import. | Generic | many |
| export_routing_policies | Export Routing Policies | RoutingPolicyBGP | bgp__export_policies | The routing-policies used by this instance for export. | Generic | many |

### RoutingBGPSession
#### Attributes
| name | kind | state |
| ---- | ---- | ----- |
| import_policies | Text | absent |
| export_policies | Text | absent |

#### Relationships
| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import_routing_policies | Import Routing Policies | RoutingPolicy | bgp__import_policies | The routing-policies used by this instance for import. | Generic | many |
| export_routing_policies | Export Routing Policies | RoutingPolicy | bgp__export_policies | The routing-policies used by this instance for export. | Generic | many |
