## BGP Communities

This schema extension adds the BGP Communities models.

- **Dependencies:** `base, extensions/routing`
- **Version:** 1.0

### Nodes

#### BGPCommunity

- **Description:** Defines a BGP community.
- **Label:** BGP Community
- **Icon:** iconoir:community
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value, community__value

##### Attributes

| name | kind | description | order_weight | optional |
| ---- | ---- | ----------- | ------------ | -------- |
| name | Text | The name of the BGP community\. | 1000 |  |
| description | Text | An optional description of the BGP community\. | 1100 | True |
| community | Text | The value of the BGP community \(RFC1997, RFC4360, RFC8092\)\. | 1200 |  |

#### Relationships

| name | label | peer | description | kind | cardinality | optional | order_weight |
| ---- | ----- | ---- | ----------- | ---- | ----------- | -------- | ------------ |
| routing\_policy | Routing Policies | RoutingPolicy | The BGP Policies using this BGP Community\. | Generic | many |  |  |
| tags |  | BuiltinTag |  | Attribute | many | True | 3000 |
