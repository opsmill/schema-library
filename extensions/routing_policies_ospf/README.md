# Routing Policies OSPF

This extension is using the Routing Policies extensions and the Routing OSPF one together.

Dependencies: `base, extensions/routing, extensions/routing_policies, extensions/routing_ospf`

## routing_policies_ospf

- **Version:** 1.0

## Nodes

### PolicyOSPF

- **Description:** A routing policiers for OSPF
- **Label:** OSPF Routing Policies
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌

## Extensions

### RoutingOSPF

#### Attributes

| name | kind | state |
| ---- | ---- | ----- |
| import\_policies | Text | absent |
| export\_policies | Text | absent |

#### Relationships

| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import\_routing\_policies | Import Routing Policies | RoutingPolicyOSPF | ospf\_\_import\_policies | The routing\-policies used by this instance for import\. | Generic | many |
| export\_routing\_policies | Export Routing Policies | RoutingPolicyOSPF | ospf\_\_export\_policies | The routing\-policies used by this instance for export\. | Generic | many |
