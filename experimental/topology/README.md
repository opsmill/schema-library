## Topology

A schema for defining and managing network topology, strategies, and services.

- **Dependencies:** `base`
- **Version:** 1.0

### Generics

#### ManagementServer

- **Description:** Generic model for network management server (dns, ntp, and dhcp).
- **Label:** Network Management Servers
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | order_weight | optional | choices |
| ---- | ---- | ------------ | -------- | ------- |
| name | Text | 1000 |  | \`\` |
| description | Text | 1100 | True | \`\` |
| status | Dropdown |  |  | \`active, provisioning, maintenance, drained\` |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| location | LocationGeneric | True | many |  |
| ip\_addresses | InfraIPAddress | True | many | Component |

#### GenericElement

- **Description:** Base model for elements
- **Label:** Generic Topology Element
- **Icon:** carbon:network-3-reference
- **Menu Placement:** TopologyTopology
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| name | Text | 1000 |  |
| description | Text | 1100 | True |
| quantity | Number | 1200 |  |

#### Relationships

| name | peer | cardinality | kind | optional |
| ---- | ---- | ----------- | ---- | -------- |
| topology | TopologyTopology | one | Parent | False |

#### NetworkStrategy

- **Description:** Generic model for network strategies (underlays and overlays).
- **Label:** Network Strategy
- **Icon:** iconoir:strategy
- **Menu Placement:** TopologyTopology
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| name | Text | 1000 |  |
| description | Text | 1100 | True |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| topology | TopologyTopology | True | many |

### Nodes

#### Topology

- **Description:** A Topology represents the entire network pod.
- **Label:** Topology
- **Icon:** carbon:network-3
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 1100 | True |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| elements | TopologyGenericElement | True | many | Component |
| strategy | TopologyNetworkStrategy | True | one | Component |
| location | LocationGeneric | True | one | Attribute |
| devices | DcimGenericDevice | True | many | Component |
| network\_services | TopologyNetworkService | True | many | Component |

#### MPLSStrategy

- **Description:** Specific strategy attributes for MPLS.
- **Label:** MPLS Strategy
- **Icon:** eos-icons:neural-network
- **Menu Placement:** TopologyNetworkStrategy
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | choices |
| ---- | ---- | ------- |
| underlay | Dropdown | \`ospf, isis, bgp\` |
| overlay | Dropdown | \`ldp, rsvp, segment\_routing\` |

#### EVPNStrategy

- **Description:** Specific strategy attributes for EVPN.
- **Label:** EVPN Strategy
- **Icon:** carbon:load-balancer-network
- **Menu Placement:** TopologyNetworkStrategy
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | choices |
| ---- | ---- | ------- |
| underlay | Dropdown | \`ebgp, ospf, isis\` |
| overlay | Dropdown | \`ebgp, ibgp\` |

#### PhysicalElement

- **Description:** Physical aspect of topology elements.
- **Label:** Physical Topology Element
- **Icon:** carbon:network-3-reference
- **Menu Placement:** TopologyTopology
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | default_value | order_weight | label | choices |
| ---- | ---- | ------------- | ------------ | ----- | ------- |
| mtu | Number | 1500 | 3000 |  | \`\` |
| border | Boolean | False | 2400 | Is a Topology Border | \`\` |
| mlag\_support | Boolean | False | 2500 | MLAG Support | \`\` |
| device\_role | Dropdown |  | 1300 | Role | \`spine, leaf, pe\_router, p\_router, route\_reflector, cpe, firewall\` |

#### Relationships

| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| device\_type | Type | DcimDeviceType | True | one | Attribute | 1400 |

#### DhcpOption

- **Description:** Represents a configurable option within a Dhcp server.
- **Label:** Dhcp Option
- **Icon:** gis:globe-options
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| name | Text | 1000 |  |
| description | Text | 1100 | True |
| option\_code | Number | 2000 |  |
| content | Text | 2100 |  |

#### DhcpServer

- **Description:** Represents a Dhcp server in the network.
- **Label:** Dhcp Server
- **Icon:** eos-icons:ip
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | order_weight |
| ---- | ---- | ------------ |
| lease\_time | Text | 2100 |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| dhcp\_options | NetworkDhcpOption | True | many | Component |

#### NameServer

- **Description:** Represents a DNS server in the network.
- **Label:** DNS Server
- **Icon:** eos-icons:dns
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### NTPServer

- **Description:** Represents a NTP server in the network.
- **Label:** NTP Server
- **Icon:** iconoir:time-zone
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### NetworkServiceIdentifier

- **Description:** Generic model for different types of identifiers used in network services.
- **Label:** Network Service Identifier
- **Icon:** mdi:identifier
- **Menu Placement:** TopologyNetworkService
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**identifier__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind |
| ---- | ---- |
| identifier | Number |

#### Relationships

| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| service | Network Service | TopologyNetworkService | one | True |

#### NetworkService

- **Description:** Network services attached to a Topology.
- **Label:** Network Service
- **Icon:** carbon:ibm-cloud-internet-services
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | label | kind | order_weight | enum |
| ---- | ----- | ---- | ------------ | ---- |
| name | Service Name | Text | 1000 |  |
| description |  | Text | 1100 |  |
| service\_type |  | Text | 1200 | \['Layer2', 'Layer3'\] |

#### Relationships

| name | peer | cardinality | kind | optional | order_weight |
| ---- | ---- | ----------- | ---- | -------- | ------------ |
| identifier | TopologyNetworkServiceIdentifier | one | Attribute | False |  |
| topology | TopologyTopology | one | Parent | False |  |
| vlan | InfraVLAN | one | Component | True | 1500 |
| prefix | InfraPrefix | one | Component | True | 1400 |

### Extensions

#### DcimGenericDevice

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| topology | TopologyTopology | True | one |

#### IpamPrefix

#### Relationships

| name | label | peer | optional | cardinality | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ------------ |
| network\_service | Network Service | TopologyNetworkService | True | one | 1400 |
