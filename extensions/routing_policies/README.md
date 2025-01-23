# Routing Policies

This schema extension contains a generic to create Routing Policies.

This Generic can be extend for each Routing Protocols you may want to use.


Dependencies: `base`

## Overview

- **Version:** 1.0

## Generics

### Policy

- **Description:** Policy defining the rules for routing traffic in a network.
- **Icon:** carbon:deployment-policy
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value
#### Attributes

| name | kind | description | unique | optional | order_weight | label | choices | default_value |
| ---- | ---- | ----------- | ------ | -------- | ------------ | ----- | ------- | ------------- |
| name | Text | The name of the routing policy. | True | False | 1000 |  | `` |  |
| description | Text | An optional description of the routing policy. |  | True | 1100 |  | `` |  |
| policy_type | Dropdown | The type of routing policy which specifies the direction of route advertisement. |  |  | 1200 | Type | `import-policy, export-policy, import-export-policy` |  |
| weight | Number | Priority of the routing policy. The higher the number, the higher the priority. |  | True | 1400 |  | `` | 1000 |
| address_family | Dropdown | The address family for the routing policy indicating the type of IP address. |  |  | 1150 |  | `ipv4, ipv6, all` | all |
