## VLAN

This schema extension contains models to support VLANs in you network.

- **Dependencies:** `base`
- **Version:** 1.0

### Nodes

#### VLAN

- **Description:** A VLAN is isolated layer two domain
- **Label:** VLAN
- **Icon:** mdi:lan-pending
- **Menu Placement:** IpamL2Domain
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**l2domain + vlan_id__value

##### Attributes

| name | kind | optional | choices |
| ---- | ---- | -------- | ------- |
| name | Text |  | \`\` |
| description | Text | True | \`\` |
| vlan\_id | Number |  | \`\` |
| status | Dropdown |  | \`active, provisioning, maintenance, drained\` |
| role | Dropdown | True | \`server, management, user\` |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| location | LocationHosting | True | many |  |  |
| prefixes | IpamPrefix | True | many |  |  |
| l2domain | IpamL2Domain | False | one | Attribute | 1200 |

#### L2Domain

- **Description:** Represents layer 2 domain.
- **Label:** Layer 2 Domain
- **Icon:** mdi:domain-switch
- **Include in Menu:** ❌

##### Attributes

| name | kind | order_weight |
| ---- | ---- | ------------ |
| name | Text | 1000 |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| vlans | IpamVLAN | True | many | Component |

### Extensions

#### IpamPrefix

#### Relationships

| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| vlan | IpamVLAN | True | one | Attribute | 1400 |

#### InterfaceLayer2

#### Relationships

| name | label | peer | optional | cardinality | kind | identifier |
| ---- | ----- | ---- | -------- | ----------- | ---- | ---------- |
| untagged\_vlan | Untagged VLAN | IpamVLAN | True | one | Generic | interface\_l2\_\_untagged\_vlan |
| tagged\_vlan | Tagged VLANs | IpamVLAN | True | many | Generic | interface\_l2\_\_tagged\_vlan |

#### LocationHosting

#### Relationships

| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| vlans | VLANs | IpamVLAN | many | True |
