# VRF

This schema extension contains models to support VRF in your network.

Dependencies: `base`

## Overview

- **Version:** 1.0

## Nodes

### VRF

- **Description:** A VRF is isolated layer three domain
- **Label:** VRF
- **Icon:** mdi:router
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | optional | unique | label | order_weight |
| ---- | ---- | -------- | ------ | ----- | ------------ |
| name | Text | False | True |  |  |
| vrf\_rd | Text | True |  | Route Distinguisher |  |
| description | Text | True |  |  | 1200 |

#### Relationships

| name | peer | optional | cardinality | kind | identifier | label |
| ---- | ---- | -------- | ----------- | ---- | ---------- | ----- |
| namespace | BuiltinIPNamespace | False | one | Attribute |  |  |
| import\_rt | IpamRouteTarget | True | one | Attribute | vrf\_\_import | Import Targets |
| export\_rt | IpamRouteTarget | True | one | Attribute | vrf\_\_export | Export Targets |

### RouteTarget

- **Description:** Route Target (RFC 4360)
- **Label:** Route Target
- **Icon:** mdi:target
- **Menu Placement:** IpamVRF
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | unique | optional |
| ---- | ---- | ------ | -------- |
| name | Text | True |  |
| description | Text |  | True |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| vrf | IpamVRF | True | many |

## Extensions

### IpamPrefix

#### Relationships

| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| vrf | VRF | IpamVRF | True | one | Attribute | 1150 |

### IpamIPAddress

#### Relationships

| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| vrf | VRF | IpamVRF | True | one | Attribute | 1150 |
