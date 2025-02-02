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
| import\_policies | Text | absent |
| export\_policies | Text | absent |

#### Relationships

| name | label | peer | identifier | description | kind | cardinality |
| ---- | ----- | ---- | ---------- | ----------- | ---- | ----------- |
| import\_routing\_policies | Import Routing Policies | RoutingPolicyAggregate | aggregate\_\_import\_policies | The routing\-policies used by this instance for import\. | Generic | many |
| export\_routing\_policies | Export Routing Policies | RoutingPolicyAggregate | aggregate\_\_export\_policies | The routing\-policies used by this instance for export\. | Generic | many |
