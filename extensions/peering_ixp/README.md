## Exchange Points (IXP)

This schema extension contains all you need to model anything revolving around internet peering (Exchange points ...)!

- **Dependencies:** `base, extensions/routing, extensions/routing_bgp, extensions/routing_bgp_community`
- **Version:** 1.0

### Nodes

#### IXP

- **Description:** An Internet Exchange Point (IXP) for peering
- **Label:** Internet Exchange
- **Icon:** mdi:network
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | unique | description | order_weight | optional | choices | default_value |
| ---- | ---- | ------ | ----------- | ------------ | -------- | ------- | ------------- |
| name | Text | True | Name of the Internet Exchange | 1000 |  | \`\` |  |
| description | Text |  | An optional description of the Internet Exchange | 1100 | True | \`\` |  |
| status | Dropdown |  |  | 1200 |  | \`enabled, disabled\` | enabled |

#### Relationships

| name | peer | optional | cardinality | kind | description | order_weight | label | identifier |
| ---- | ---- | -------- | ----------- | ---- | ----------- | ------------ | ----- | ---------- |
| connections | PeeringIXPConnection | True | many | Component | IXP connections associated with this Internet Exchange |  |  |  |
| local\_as | RoutingAutonomousSystem | True | one | Attribute |  | 1300 |  |  |
| import\_policies | RoutingPolicyBGP | True | many | Generic | Import routing policies applied to the session |  | Import Routing Policies | ixp\_\_import\_bgppolicies |
| export\_policies | RoutingPolicyBGP | True | many | Generic | Export routing policies applied to the session |  | Export Routing Policies | ixp\_\_export\_bgppolicies |
| bgp\_communities | RoutingBGPCommunity | True | many | Generic | BGP communities associated with the session |  | BGP Communities |  |
| tags | BuiltinTag | True | many | Attribute |  | 3000 |  |  |

#### IXPConnection

- **Description:** A connection to an Internet Exchange Point (IXP)
- **Label:** IXP Connection
- **Icon:** mdi:lan-connect
- **Menu Placement:** PeeringIXP
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | unique | description | order_weight | optional | label | choices | default_value |
| ---- | ---- | ------ | ----------- | ------------ | -------- | ----- | ------- | ------------- |
| name | Text | True | Name of the IXP Connection | 1000 |  |  | \`\` |  |
| description | Text |  | Description of the IXP Connection | 1100 | True |  | \`\` |  |
| peeringdb\_netixlan | Number |  | PeeringDB ID for the IXP connection | 1150 | True | PeeringDB Netixlan | \`\` |  |
| status | Dropdown |  |  | 1200 | True |  | \`enabled, pre\-maintenance, maintenance, post\-maintenance, disabled\` | enabled |
| vlan | Number |  | VLAN ID for the connection | 1300 | True |  | \`\` |  |
| mac\_address | MacAddress |  | MAC address associated with the connection | 1350 | True | MAC Address | \`\` |  |

#### Relationships

| name | label | description | peer | identifier | cardinality | kind | order_weight | optional |
| ---- | ----- | ----------- | ---- | ---------- | ----------- | ---- | ------------ | -------- |
| ipv6\_address | IPv6 Address | IPv6 address assigned to the connection | IpamIPAddress | ixpconn\_\_ipv6\_address | one | Attribute | 1400 |  |
| ipv4\_address | IPv4 Address | IPv4 address assigned to the connection | IpamIPAddress | ixpconn\_\_ipv4\_address | one | Attribute | 1375 |  |
| internet\_exchange\_point | IXP | The Internet Exchange Point this connection is part of | PeeringIXP |  | one | Parent |  | False |
| router |  | The router this IXP connection is connected to | DcimDevice |  | one | Attribute | 1400 |  |
| tags |  |  | BuiltinTag |  | many | Attribute | 3000 |  |
