# VLAN Translation

This schema extension is based on Juniper VLAN MAP, and not yet test out for other vendors.

Dependencies: `base`

## vlan-translation

- **Version:** 1.0

## Nodes

### MapInOut

- **Description:** VLAN Mapping for In/Out operations
- **Label:** VLAN Map In/Out
- **Icon:** ph:swap
- **Menu Placement:** DcimInterface
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**interface__name__value, direction__value, operation__value
- **Uniqueness Constraints:**interface + direction__value

#### Attributes

| name | kind | description | label | order_weight | choices | optional |
| ---- | ---- | ----------- | ----- | ------------ | ------- | -------- |
| direction | Dropdown | Direction of the mapping | Map Direction | 1050 | \`input, output\` | True |
| operation | Dropdown | Operation type | Map Operation | 1100 | \`pop, pop\_pop, pop\_swap, push, push\_push, swap, swap\_push, swap\_swap\` | True |
| vlan\_id\_swap | Number | VLAN ID to swap to during SWAP operations | VLAN ID Swap | 1200 | \`\` | True |
| inner\_vlan\_id | Number | Inner VLAN ID for operations involving double VLAN tags | Inner VLAN ID | 1300 | \`\` | True |
| inner\_tag\_protocol\_id | Number | Inner tag protocol ID \(TPID\) | Inner Tag Protocol ID | 1400 | \`\` | True |
| tag\_protocol\_id | Number | Tag protocol ID \(TPID\) for outer VLAN operations | Tag Protocol ID | 1500 | \`\` | True |

#### Relationships

| name | kind | peer | description | cardinality | optional | label | order_weight |
| ---- | ---- | ---- | ----------- | ----------- | -------- | ----- | ------------ |
| interface | Parent | DcimInterface | Interface to which the Input/Output VLAN mapping is applied | one | False | Interface | 1000 |

## Extensions

### DcimInterface

#### Relationships

| name | kind | peer | description | cardinality | label | order_weight |
| ---- | ---- | ---- | ----------- | ----------- | ----- | ------------ |
| network\_maps | Component | NetworkMapInOut | Interface Input/Output VLAN mapping | many | Input/Output MAP | 1600 |
