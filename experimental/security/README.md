# Security

This schema extension contains models for implementing detailed security.

Dependencies: `base`

## security

- **Version:** 1.0

## Generics

### PolicyAssignment

- **Label:** Security Policy
- **Include in Menu:** ❌

#### Relationships

| name | label | peer | kind | cardinality | optional |
| ---- | ----- | ---- | ---- | ----------- | -------- |
| rules | Policy | SecurityRenderedPolicyRule | Component | many | True |

### GenericAddressGroup

- **Include in Menu:** ❌

#### Attributes

| name | kind | label | optional | unique |
| ---- | ---- | ----- | -------- | ------ |
| name | Text | Name | False | True |
| description | Text | Description | True |  |

#### Relationships

| name | peer | cardinality | kind | optional |
| ---- | ---- | ----------- | ---- | -------- |
| addresses | SecurityGenericAddress | many | Component | True |

### GenericAddress

- **Include in Menu:** ❌

#### Attributes

| name | kind | optional | unique |
| ---- | ---- | -------- | ------ |
| name | Text | False | True |

#### Relationships

| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| address\_groups | Address Groups | SecurityGenericAddressGroup | many | True |

### GenericServiceGroup

- **Include in Menu:** ❌

#### Attributes

| name | label | kind | optional |
| ---- | ----- | ---- | -------- |
| name | Name | Text | False |
| description | Description | Text | True |

#### Relationships

| name | peer | label | cardinality | kind | optional |
| ---- | ---- | ----- | ----------- | ---- | -------- |
| services | SecurityGenericService | Services | many | Component | True |

### GenericService

- **Include in Menu:** ❌

#### Attributes

| name | label | kind | optional |
| ---- | ----- | ---- | -------- |
| name | Name | Text | False |
| description | Description | Text | True |

#### Relationships

| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| service\_groups | Service Groups | SecurityGenericServiceGroup | many | True |

## Nodes

### Zone

- **Description:** Security zones
- **Label:** Security zone
- **Icon:** game-icons:fire-zone
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Attributes

| name | kind | unique | optional |
| ---- | ---- | ------ | -------- |
| name | Text | True | False |

#### Relationships

| name | label | kind | optional | peer |
| ---- | ----- | ---- | -------- | ---- |
| interfaces | Interfaces | Attribute | True | SecurityFirewallInterface |

### IPAMIPAddress

- **Description:** Infrahub IPv4/6 address
- **Label:** IPAM IP Address
- **Icon:** mdi:ip-outline
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Attributes

| name | kind | optional |
| ---- | ---- | -------- |
| description | Text | True |

#### Relationships

| name | peer | cardinality | kind | optional |
| ---- | ---- | ----------- | ---- | -------- |
| ip\_address | InfraIPAddress | one | Attribute | False |

### IPAMIPPrefix

- **Description:** Infrahub IPv4/6 prefix
- **Label:** IPAM IP Prefix
- **Icon:** mdi:ip-network-outline
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Attributes

| name | kind | optional |
| ---- | ---- | -------- |
| description | Text | True |

#### Relationships

| name | peer | cardinality | kind | optional |
| ---- | ---- | ----------- | ---- | -------- |
| ip\_prefix | InfraPrefix | one | Attribute | False |

### IPAddress

- **Description:** IPv4/6 address
- **Label:** IP Address
- **Icon:** mdi:ip-outline
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**address__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | optional |
| ---- | ---- | -------- |
| address | IPHost |  |
| description | Text | True |

### Prefix

- **Description:** IPv4/6 prefix
- **Label:** Prefix
- **Icon:** mdi:ip-network-outline
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | optional | unique |
| ---- | ---- | -------- | ------ |
| prefix | IPNetwork | False | True |
| description | Text | True |  |

### IPRange

- **Description:** IPv4/6 Range
- **Label:** IP Range
- **Icon:** mdi:ip-outline
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | label | kind | optional |
| ---- | ----- | ---- | -------- |
| start | Start IP Address | IPHost | False |
| end | End IP Address | IPHost | False |

### FQDN

- **Description:** Full Qualified Domain Name
- **Label:** FQDN
- **Icon:** eos-icons:dns
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value, fqdn__value
- **Uniqueness Constraints:**

#### Attributes

| name | label | kind | optional | regex |
| ---- | ----- | ---- | -------- | ----- |
| fqdn | FQDN | Text | False | \(?=^\.{1,253}\$\)\(^\(\(\(?\!\-\)\[a\-zA\-Z0\-9\-\]{1,63}\(?\<\!\-\)\)\|\(\(?\!\-\)\[a\-zA\-Z0\-9\-\]{1,63}\(?\<\!\-\)\\.\)\+\[a\-zA\-Z\]{2,63}\)\$\) |

### AddressGroup

- **Description:** Group of addresses
- **Label:** Address Group
- **Icon:** material-symbols:menu-book-outline-rounded
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

### IPProtocol

- **Description:** IP protocol
- **Label:** IP Protocols
- **Icon:** mdi:protocol
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | optional |
| ---- | ---- | -------- |
| protocol | Number | True |

### Service

- **Description:** Service
- **Label:** Service
- **Icon:** eos-icons:application-outlined
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind |
| ---- | ---- |
| port | Number |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| ip\_protocol | SecurityIPProtocol | True | one | Attribute |

### ServiceRange

- **Description:** Service range
- **Label:** Service range
- **Icon:** eos-icons:application-outlined
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | optional |
| ---- | ---- | -------- |
| start | Number | False |
| end | Number | False |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| ip\_protocol | SecurityIPProtocol | False | one | Attribute |

### ServiceGroup

- **Description:** Group of services
- **Label:** Service group
- **Icon:** material-symbols:menu-book-outline-rounded
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

### Policy

- **Label:** Security Policy
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | label | kind | optional |
| ---- | ----- | ---- | -------- |
| name | Name | Text | False |
| description | Description | Text | True |

#### Relationships

| name | peer | cardinality | kind | optional |
| ---- | ---- | ----------- | ---- | -------- |
| rules | SecurityPolicyRule | many | Component |  |
| location\_target | LocationGeneric | one | Attribute | True |
| device\_target | SecurityFirewall | one | Attribute | True |

### PolicyRule

- **Description:** Policy rule
- **Label:** Policy rule
- **Icon:** material-symbols:policy
- **Menu Placement:** SecurityPolicy
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**source_zone__name__value, destination_zone__name__value, index__value
- **Uniqueness Constraints:**index__value + source_zone + destination_zone + policy

#### Attributes

| name | label | kind | optional | order_weight | enum | default_value |
| ---- | ----- | ---- | -------- | ------------ | ---- | ------------- |
| index | Index | Number | False | 99999 |  |  |
| name | Name | Text | False |  |  |  |
| action | Action | Text | False |  | \['permit', 'deny'\] | permit |
| log | Log | Boolean | True | 99998 |  | False |

#### Relationships

| name | peer | kind | cardinality | optional | order_weight | identifier |
| ---- | ---- | ---- | ----------- | -------- | ------------ | ---------- |
| policy | SecurityPolicy | Attribute | one | False |  |  |
| source\_zone | SecurityZone | Attribute | one | False | 1 | policy\_rule\_\_source\_zone |
| destination\_zone | SecurityZone | Attribute | one | False | 2 | policy\_rule\_\_destination\_zone |
| source\_address | SecurityGenericAddress | Attribute | many | True |  | policy\_rule\_\_source\_address |
| source\_groups | SecurityGenericAddressGroup | Attribute | many | True |  | policy\_rule\_\_source\_address\_group |
| source\_services | SecurityGenericService | Attribute | many | True |  | policy\_rule\_\_source\_service |
| source\_service\_groups | SecurityGenericServiceGroup | Attribute | many | True |  | policy\_rule\_\_source\_service\_group |
| destination\_address | SecurityGenericAddress | Attribute | many | True |  | policy\_rule\_\_destination\_address |
| destination\_groups | SecurityGenericAddressGroup | Attribute | many | True |  | policy\_rule\_\_destination\_address\_group |
| destination\_services | SecurityGenericService | Attribute | many | True |  | policy\_rule\_\_destination\_service |
| destination\_service\_groups | SecurityGenericServiceGroup | Attribute | many | True |  | policy\_rule\_\_destination\_service\_group |

### Firewall

- **Icon:** mdi:firewall
- **Menu Placement:** InfraGenericDevice
- **Include in Menu:** ✅

#### Attributes

| name | kind | optional | choices |
| ---- | ---- | -------- | ------- |
| role | Dropdown | True | \`edge\_firewall\` |

#### Relationships

| name | peer | label | cardinality | kind |
| ---- | ---- | ----- | ----------- | ---- |
| policy | SecurityPolicy | Security Policy | one | Attribute |

### RenderedPolicyRule

- **Description:** Policy rule
- **Label:** Policy rule
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**source_zone__name__value, destination_zone__name__value, index__value
- **Uniqueness Constraints:**

#### Attributes

| name | label | kind | optional | order_weight | enum | default_value |
| ---- | ----- | ---- | -------- | ------------ | ---- | ------------- |
| index | Index | Number | False | 99999 |  |  |
| name | Name | Text | False |  |  |  |
| action | Action | Text | False |  | \['permit', 'deny'\] | permit |
| log | Log | Boolean | True | 99998 |  | False |

#### Relationships

| name | peer | kind | cardinality | optional | identifier | order_weight |
| ---- | ---- | ---- | ----------- | -------- | ---------- | ------------ |
| source\_policy | SecurityPolicy | Attribute | one | False |  |  |
| source\_zone | SecurityZone | Attribute | one | False | rendered\_policy\_rule\_\_source\_zone | 1 |
| destination\_zone | SecurityZone | Attribute | one | False | rendered\_policy\_rule\_\_destination\_zone | 2 |
| source\_address | SecurityGenericAddress | Attribute | many | True | rendered\_policy\_rule\_\_source\_address |  |
| source\_groups | SecurityGenericAddressGroup | Attribute | many | True | rendered\_policy\_rule\_\_source\_address\_group |  |
| source\_services | SecurityGenericService | Attribute | many | True | rendered\_policy\_rule\_\_source\_service |  |
| source\_service\_groups | SecurityGenericServiceGroup | Attribute | many | True | rendered\_policy\_rule\_\_source\_service\_group |  |
| destination\_address | SecurityGenericAddress | Attribute | many | True | rendered\_policy\_rule\_\_destination\_address |  |
| destination\_groups | SecurityGenericAddressGroup | Attribute | many | True | rendered\_policy\_rule\_\_destination\_address\_group |  |
| destination\_services | SecurityGenericService | Attribute | many | True | rendered\_policy\_rule\_\_destination\_service |  |
| destination\_service\_groups | SecurityGenericServiceGroup | Attribute | many | True | rendered\_policy\_rule\_\_destination\_service\_group |  |

### FirewallInterface

- **Label:** Firewall Interface
- **Icon:** mdi:ethernet
- **Menu Placement:** InfraGenericDevice
- **Include in Menu:** ❌

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| ip\_addresses | InfraIPAddress | True | many | Component |
| security\_zone | SecurityZone | False | one | Attribute |

## Extensions

### LocationGeneric

#### Relationships

| name | peer | cardinality | kind |
| ---- | ---- | ----------- | ---- |
| policy | SecurityPolicy | one | Attribute |
