# Circuit Service

This schema extension contains model coming on top of circuit to capture a single service shared across multiple circuits.
For example you have a MPLS network supported by a provider connecting multiple locations:

- One single CircuitService would be needed to store MPLS related information (e.g. service id, provider ...)
- On each site we would create a circuit connecting on one side our device and the CircuitService on the other side

Dependencies: `extensions.circuit`

## circuit_service

- **Version:** 1.0

## Nodes

### Service

- **Description:** Represent the boundary of a provider network, the details of which are unknown or unimportant
- **Label:** Circuit Service
- **Icon:** mdi:cloud
- **Menu Placement:** DcimCircuit
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | unique | optional |
| ---- | ---- | ------ | -------- |
| name | Text | True |  |
| service\_id | Text |  | True |
| description | Text |  | True |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| provider | OrganizationProvider | False | one | Attribute |
| circuit\_endpoints | CircuitEndpoint | True | many | Component |

## Extensions

### OrganizationProvider

#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| circuit\_services | CircuitService | many | True |

### CircuitEndpoint

#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| circuit\_service | CircuitService | one | True |
