## Routing Policies (PIM)

This schema inherits the `RoutingPolicy` schema and removes `import_policies` and `export_policies` attributes. However it adds a number of relationships to `RoutingPIM`.

- **Dependencies:** `base, extensions/routing, extensions/routing_policies, extensions/routing_pim`
- **Version:** 1.0

### Nodes

#### PolicyPIM

- **Description:** A routing policiers for PIM
- **Label:** PIM Routing Policies
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌

### Extensions

#### RoutingPIM

#### Attributes

| name | kind | state |
| ---- | ---- | ----- |
| import\_policies | Text | absent |
| export\_policies | Text | absent |

#### Relationships

| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import\_routing\_policies | Import Routing Policies | RoutingPolicyPIM | pim\_\_import\_policies | The routing\-policies used by this instance for import\. | Generic | many |
| export\_routing\_policies | Export Routing Policies | RoutingPolicyPIM | pim\_\_export\_policies | The routing\-policies used by this instance for export\. | Generic | many |
