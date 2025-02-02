# Topology

This schema extension introduces abstract network pods and services running in the pods, such as MPLS and EVPN.

Dependencies: `base`

## topology

- **Version:** 1.0

## Generics

### Generic

- **Description:** Generic model for topology.
- **Label:** Topology
- **Icon:** carbon:network-3
- **Include in Menu:** ❌

#### Attributes

| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| description | Text | 1300 | True |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| location | LocationGeneric | True | one | Attribute |
