# Circuit

This schema extension contains Circuits and ways to connect them with your infrastructure! The circuit could be a fiber connecting two sites, you would then have two endpoints, one on each site.

Dependencies: `base, extensions.location_minimal`

## Overview

- **Version:** 1.0

## Nodes

### Circuit

- **Description:** A Circuit represent service operated by a provider.
- **Label:** Circuit
- **Icon:** mdi:cable-data
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** circuit_id__value
- **Uniqueness Constraints:** 
#### Attributes

| name | kind | unique | optional | description | choices |
| ---- | ---- | ------ | -------- | ----------- | ------- |
| circuit_id | Text | True |  |  | `` |
| description | Text |  | True |  | `` |
| circuit_type | Dropdown |  |  | Specifies the type of circuit. | `upstream, peering, dark_fiber, mpls` |
| status | Dropdown |  |  |  | `active, provisioning, maintenance, drained` |

#### Relationships

| name | peer | optional | cardinality | kind | label | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ----- | ------------ |
| provider | OrganizationProvider | False | one | Attribute |  |  |
| location | LocationHosting | True | one | Attribute | Location | 1500 |
| enpoints | DcimCircuitEndpoint | True | many | Component |  |  |

### CircuitEndpoint

- **Description:** A circuit endpoint, could be a position in a MMR...
- **Label:** Circuit Endpoint
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimCircuit
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** circuit + name__value
#### Attributes

| name | kind | description | order_weight | optional | choices |
| ---- | ---- | ----------- | ------------ | -------- | ------- |
| name | Text | Name of the circuit endoint, could be a MMR position for instance. | 1000 |  | `` |
| status | Dropdown |  |  | True | `active, provisioning, maintenance, drained` |
| description | Text |  |  | True | `` |

#### Relationships

| name | peer | order_weight | optional | cardinality | kind | label |
| ---- | ---- | ------------ | -------- | ----------- | ---- | ----- |
| circuit | DcimCircuit | 900 | False | one | Parent |  |
| location | LocationHosting | 1500 | False | one | Attribute | Location |

## Extensions
### OrganizationProvider
#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| circuits | DcimCircuit | many | True |

### LocationHosting
#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| circuits | DcimCircuit | many | True |
