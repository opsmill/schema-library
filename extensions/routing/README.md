# Routing

This schema extension contains generics to create Routing Protocol "Instance". The idea is to create one Routing Protocol instance per IpamVRF + DcimDevice pair.

Dependencies: `base, extensions.vlan`

## Overview

- **Version:** 1.0

## Generics

### Protocol

- **Description:** Generic protocol model for routing protocols
- **Label:** Protocol
- **Icon:** carbon:router
- **Include in Menu:** ❌

#### Attributes

| name | kind | optional | description | order_weight | choices |
| ---- | ---- | -------- | ----------- | ------------ | ------- |
| description | Text | False | Description of the protocol | 1100 | `` |
| status | Dropdown |  | Status of the Protocol Configuration. | 1150 | `active, disabled, deleted` |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight | label |
| ---- | ---- | -------- | ----------- | ---- | ------------ | ----- |
| device | DcimDevice | False | one | Parent | 1050 |  |
| vrf | IpamVRF | False | one | Attribute | 1075 | VRF |
