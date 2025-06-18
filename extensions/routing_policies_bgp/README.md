## Routing Policies BGP

This extension is using the Routing Policies extensions and the Routing BGP one together.

- **Dependencies:** `base, extensions/routing, extensions/routing_policies, extensions/routing_bgp`
- **Version:** 1.0

### Nodes

#### PolicyBGP

- **Description:** A routing policiers for BGP
- **Label:** BGP Routing Policies
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌

### Extensions

#### RoutingBGPPeerGroup

#### Attributes

| name | kind | state |
| ---- | ---- | ----- |
| import\_policies | Text | absent |
| export\_policies | Text | absent |

#### Relationships

| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import\_routing\_policies | Import Routing Policies | RoutingPolicyBGP | bgp\_\_import\_policies | The routing\-policies used by this instance for import\. | Generic | many |
| export\_routing\_policies | Export Routing Policies | RoutingPolicyBGP | bgp\_\_export\_policies | The routing\-policies used by this instance for export\. | Generic | many |

#### RoutingBGPSession

#### Attributes

| name | kind | state |
| ---- | ---- | ----- |
| import\_policies | Text | absent |
| export\_policies | Text | absent |

#### Relationships

| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import\_routing\_policies | Import Routing Policies | RoutingPolicy | bgp\_\_import\_policies | The routing\-policies used by this instance for import\. | Generic | many |
| export\_routing\_policies | Export Routing Policies | RoutingPolicy | bgp\_\_export\_policies | The routing\-policies used by this instance for export\. | Generic | many |
