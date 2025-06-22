## Interface Breakout

This schema extension introduces relationships to support breakout interfaces, enabling you to document the breakout of a physical interface into smaller physical interfaces.

- **Dependencies:** `base`
- **Version:** 1.0

### Extensions

#### InterfacePhysical

#### Attributes

| name | kind | optional | default_value | description |
| ---- | ---- | -------- | ------------- | ----------- |
| breakout\_capability | Boolean | False | False | Indicates if the port supports breakout capability |

#### Relationships

| name | peer | label | optional | cardinality | kind | identifier | direction | description | order_weight |
| ---- | ---- | ----- | -------- | ----------- | ---- | ---------- | --------- | ----------- | ------------ |
| breakout\_child\_interfaces | InterfacePhysical | Breakout child interface\(s\) | True | many | Attribute | physical\_\_breakout | outbound | Interfaces resulting from the breakout | 1650 |
| breakout\_parent\_interface | InterfacePhysical | Breakout parent interface | True | one | Attribute | physical\_\_breakout | inbound | Interface from which breakout is created | 1700 |
