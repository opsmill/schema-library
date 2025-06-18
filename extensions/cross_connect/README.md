# Cross Connect

This extension contains schema to capture Cross Connect. You can see it as "a cable operated by a provider". You will be able to attach it to a location and then connect endpoints to it (e.g. rear interface of a patch panel, circuit endpoint ...)

Dependencies: `base`

## cross_connect

- **Version:** 1.0

### Nodes

### CrossConnect

- **Description:** Cross-connect between different endpoints within a datacenter.
- **Label:** Cross-Connect
- **Icon:** streamline:arrow-crossover-right-solid
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**provider__name__value
- **Uniqueness Constraints:**provider + identifier__value

#### Attributes

| name | kind | order_weight | optional | choices |
| ---- | ---- | ------------ | -------- | ------- |
| identifier | Text | 900 |  | \`\` |
| description | Text | 1300 | True | \`\` |
| status | Dropdown | 1200 | True | \`connected, planned, reserved\` |

#### Relationships

| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| location | Location | LocationHosting | False | one | Attribute | 1100 |
| provider |  | OrganizationProvider | False | one | Attribute | 1000 |
