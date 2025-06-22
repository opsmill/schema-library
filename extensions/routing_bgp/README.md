## Routing BGP

This schema extension contains all you need to model your BGP platform.

- **Dependencies:** `base, extensions/routing`
- **Version:** 1.0

### Nodes

#### AutonomousSystem

- **Description:** An Autonomous System (AS) is a set of Internet routable IP prefixes belonging to a network
- **Label:** Autonomous System
- **Icon:** mdi:bank-circle-outline
- **Menu Placement:** RoutingBGPSession
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**asn__value, name__value
- **Uniqueness Constraints:**asn__value, name__value

##### Attributes

| name | kind | description | order_weight | optional |
| ---- | ---- | ----------- | ------------ | -------- |
| name | Text | Name of the Autonomous System | 1000 |  |
| asn | Number | Autonomous System Number | 1050 |  |
| description | Text | Description of the Autonomous System | 1100 | True |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| organization | OrganizationGeneric | False | one | Attribute |
| location | LocationGeneric | True | one | Attribute |
| devices | DcimDevice | True | many | Attribute |

#### BGPPeerGroup

- **Description:** A BGP Peer Group is used to regroup parameters that are shared across multiple peers
- **Label:** BGP Peer Group
- **Icon:** mdi:view-grid-plus-outline
- **Menu Placement:** RoutingBGPSession
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | optional | description | order_weight | regex | choices | default_value |
| ---- | ---- | -------- | ----------- | ------------ | ----- | ------- | ------------- |
| name | Text | False | Name of the BGP Group | 1000 |  | \`\` |  |
| import\_policies | Text | True |  | 1300 |  | \`\` |  |
| export\_policies | Text | True |  | 1350 |  | \`\` |  |
| maximum\_routes | Number | True | Maximum routes for the BGP Group\. | 1400 | ^\[0\-9\]\+\$ | \`\` |  |
| local\_pref | Number | True | Force Local Pref for this BGP Peer Group\. | 1450 | ^\[0\-9\]\+\$ | \`\` |  |
| send\_community | Checkbox | True | Whether to send community attributes\. | 1500 |  | \`\` |  |
| address\_family | Dropdown |  | The address family for the routing policy indicating the type of IP address\. | 1150 |  | \`ipv4, ipv6\` | ipv4 |

#### Relationships

| name | identifier | peer | optional | cardinality | kind |
| ---- | ---------- | ---- | -------- | ----------- | ---- |
| local\_as | bgppeergroup\_\_local\_as | RoutingAutonomousSystem | True | one | Attribute |
| remote\_as | bgppeergroup\_\_remote\_as | RoutingAutonomousSystem | True | one | Attribute |

#### BGPSession

- **Description:** A BGP Session represent a point to point connection between two routers
- **Label:** BGP Session
- **Icon:** mdi:router
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**remote_as__asn__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | optional | enum | description | order_weight | choices | regex |
| ---- | ---- | -------- | ---- | ----------- | ------------ | ------- | ----- |
| import\_policies | Text | True |  |  |  | \`\` |  |
| export\_policies | Text | True |  |  |  | \`\` |  |
| session\_type | Text |  | \['EXTERNAL', 'INTERNAL'\] | Type of BGP Session | 1200 | \`\` |  |
| role | Dropdown |  |  | Role of the BGP Session | 1600 | \`backbone, upstream, peering\` |  |
| local\_pref | Number | True |  | Force Local Pref for this BGP Peer Session\. | 1450 | \`\` | ^\[0\-9\]\+\$ |

#### Relationships

| name | identifier | peer | optional | cardinality | kind |
| ---- | ---------- | ---- | -------- | ----------- | ---- |
| local\_as | bgpsession\_\_local\_as | RoutingAutonomousSystem | True | one | Attribute |
| remote\_as | bgpsession\_\_remote\_as | RoutingAutonomousSystem | True | one | Attribute |
| local\_ip | bgpsession\_\_local\_ip | IpamIPAddress | True | one | Attribute |
| remote\_ip | bgpsession\_\_remote\_ip | IpamIPAddress | True | one | Attribute |
| device |  | DcimDevice | True | one |  |
| peer\_group |  | RoutingBGPPeerGroup | True | one | Attribute |
| peer\_session |  | RoutingBGPSession | True | one | Attribute |

### Extensions

#### DcimGenericDevice

#### Relationships

| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| asn | RoutingAutonomousSystem | True | one | Attribute | 1600 |

#### OrganizationGeneric

#### Relationships

| name | label | cardinality | optional | peer | order_weight |
| ---- | ----- | ----------- | -------- | ---- | ------------ |
| asn | Autonomous System | many | True | RoutingAutonomousSystem | 2000 |
