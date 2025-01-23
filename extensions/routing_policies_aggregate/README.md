# Routing Policies Aggregate

This extension is using the Routing Policies extensions and the Routing Aggregate one together.

Dependencies: `base, extensions.routing, extensions.routing_policies, extensions.routing_aggregate`

## Overview

- **Version:** 1.0

## Nodes

### PolicyAggregate

- **Description:** A routing policiers for Aggregate
- **Label:** Aggregate Routing Policies
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌

## Extensions
### RoutingAggregate
#### Attributes

| name | kind | state |
| ---- | ---- | ----- |
| import_policies | Text | absent |
| export_policies | Text | absent |

#### Relationships

| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import_routing_policies | Import Routing Policies | RoutingPolicyAggregate | aggregate__import_policies | The routing-policies used by this instance for import. | Generic | many |
| export_routing_policies | Export Routing Policies | RoutingPolicyAggregate | aggregate__export_policies | The routing-policies used by this instance for export. | Generic | many |
