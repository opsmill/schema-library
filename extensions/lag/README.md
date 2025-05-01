# Lag

This schema extension includes models for Link Aggregation Groups (LAGs), enabling you to link physical interfaces as building blocs of your LAG interface. It can be used in standard networking environments as well as in compute scenarios, such as capturing bond interfaces.

Dependencies: `base`

## lag

- **Version:** 1.0

## Nodes

### Lag

- **Description:** LAG interface
- **Label:** LAG Interface
- **Include in Menu:** ❌

#### Attributes

| name | label | kind | choices | default_value | description | order_weight |
| ---- | ----- | ---- | ------- | ------------- | ----------- | ------------ |
| lacp\_rate | LACP Rate | Dropdown | \`slow, fast\` | fast | LACP rate for the aggregated interface | 1700 |
| lacp\_mode | LACP Mode | Dropdown | \`active, passive, disabled\` | active | LACP mode for the aggregated interface | 1750 |

#### Relationships

| name | label | peer | cardinality | kind | description | order_weight |
| ---- | ----- | ---- | ----------- | ---- | ----------- | ------------ |
| lag\_members | Member\(s\) | InterfacePhysical | many | Attribute | Physical Interfaces that are members of this aggregate | 1800 |

## Extensions

### InterfacePhysical

#### Relationships

| name | label | peer | optional | cardinality | kind | description | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ----------- | ------------ |
| lag\_parent | LAG | InterfaceLag | True | one | Attribute | LAG Interface using this Physical Interface | 1800 |
