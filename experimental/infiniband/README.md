## Infiniband

This schema extension adds support for InfiniBand switches.

- **Dependencies:** `base, extensions/compute`
- **Version:** 1.0

### Nodes

#### Switch

- **Description:** InfiniBand Switch
- **Label:** InfiniBand Switch
- **Icon:** mdi:server
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | unique | order_weight | optional | label | description | default_value | choices |
| ---- | ---- | ------ | ------------ | -------- | ----- | ----------- | ------------- | ------- |
| name | Text | True | 1000 |  |  |  |  | \`\` |
| description | Text |  | 2000 | True |  |  |  | \`\` |
| os\_version | Text |  | 2200 | True |  |  |  | \`\` |
| rsu\_rail\_id | Number |  |  | True | RSU Rail ID | InfiniBand RSU Rail ID \(numeric\) assigned to the switch |  | \`\` |
| aaa\_authentication\_model | Dropdown |  |  | False | AAA Authentication Model | AAA authentication model to be used by the switch | local | \`tacacs, local\` |
| aaa\_accounting\_model | Dropdown |  |  | False | AAA Accounting Model | AAA accounting model to be used by the switch | local | \`tacacs, local\` |
| role | Dropdown |  |  |  | Switch Role | Role of the switch in the InfiniBand network |  | \`spine, leaf\` |
| split\_ready | Boolean |  |  |  | Split Ready | Enable Split\-Ready profile for switch | False | \`\` |
| ipv6\_enable | Boolean |  |  |  | IPv6 Enable | Enable IPv6 on the switch | False | \`\` |
| cli\_prefix\_modes | Boolean |  |  |  | CLI Prefix Modes | Enable CLI prefix modes | True | \`\` |
| xml\_gateway | Boolean |  |  |  | XML Gateway | Enable XML Gateway | False | \`\` |
| ssh\_server\_security\_strict | Boolean |  |  |  | SSH Server Security Strict | Enable SSH Server Security Strict | False | \`\` |
| banner | Text |  |  |  | Banner | Banner to be displayed on login | NVIDIA MLNX\-OS Switch Management | \`\` |
| password\_hardening | Boolean |  |  |  | Password Hardening | Enable Password Hardening | False | \`\` |

#### Relationships

| name | kind | cardinality | peer | optional |
| ---- | ---- | ----------- | ---- | -------- |
| interfaces | Component | many | InfinibandSwitchInterface | True |
| mgmt\_interface | Component | one | InfinibandSwitchMgmtInterface | True |
| rsu | Attribute | one | InfinibandRSU | True |

#### SwitchInterface

- **Description:** InfiniBand Switch Interface
- **Label:** InfiniBand Switch Interface
- **Icon:** mdi:ethernet
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**switch + name__value

##### Attributes

| name | kind | order_weight | optional | default_value | label | description | enum | choices |
| ---- | ---- | ------------ | -------- | ------------- | ----- | ----------- | ---- | ------- |
| name | Text | 1000 |  |  |  |  |  | \`\` |
| description | Text | 1100 | True |  |  |  |  | \`\` |
| speed | Number | 1400 |  |  |  |  |  | \`\` |
| enabled | Boolean | 1200 |  | True |  |  |  | \`\` |
| width | Number |  | True | 7 | Width | Width value sets supported lane options for the interface | \[1, 3, 5, 7\] | \`\` |
| port\_type | Number |  | True |  | Port Type: Split | Enable interface to be split X times \(requires Split\-Ready profile to be enabled on the switch\) | \[2\] | \`\` |
| port\_type\_force | Boolean |  |  | False | Port Type Force | Force the configured port type setting; use in conjunction with Port Type |  | \`\` |
| operational\_virtual\_lanes | Number |  |  | 8 | Operational Virtual Lanes | Number of operational virtual lanes for an interface | \[1, 2, 4, 8\] | \`\` |
| mtu | Number |  |  |  | MTU \(bytes\) | Maximum Transmission Unit \(bytes\) | \[256, 512, 1024, 2048, 4096\] | \`\` |
| speed\_forced | Boolean |  |  | False | Speed Forced | Force the configured speed setting\(s\); use in conjunction with Speed options |  | \`\` |
| sfp\_type | Text |  | True |  | SFP Type | Type of SFP module used in the interface |  | \`\` |
| role | Dropdown |  | True |  | Interface Role | Role of the interface in the InfiniBand network |  | \`endhost, uplink, reserved\` |

#### Relationships

| name | peer | optional | cardinality | kind | max_count |
| ---- | ---- | -------- | ----------- | ---- | --------- |
| speed\_option | InfinibandSwitchIntfSpeedOptions | True | many | Attribute | 6 |
| switch | InfinibandSwitch | False | one | Parent |  |

#### SwitchMgmtInterface

- **Description:** InfiniBand Switch Management Interface
- **Label:** InfiniBand Mgmt Interface
- **Icon:** mdi:ethernet
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**switch + name__value

##### Attributes

| name | kind | order_weight | optional | label | default_value | description |
| ---- | ---- | ------------ | -------- | ----- | ------------- | ----------- |
| name | Text | 1000 |  |  |  |  |
| description | Text | 1100 | True |  |  |  |
| speed | Number | 1400 |  |  |  |  |
| mtu | Number | 1500 |  | MTU | 1500 |  |
| enabled | Boolean | 1200 |  |  | True |  |
| dhcp | Boolean |  |  | DHCP | True | Enable DHCP for the management interface |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| switch | InfinibandSwitch | False | one | Parent |
| ipv4\_address | IpamIPAddress | True | one |  |

#### SwitchIntfSpeedOptions

- **Description:** InfiniBand Interface Speed Options
- **Label:** InfiniBand Interface Speed Options
- **Icon:** mdi:ethernet
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**speed__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | label | description | choices | unique |
| ---- | ---- | ----- | ----------- | ------- | ------ |
| speed | Dropdown | Speed | Speed of the interface | \`SDR, NDR, QDR, FDR, EDR, HDR\` |  |
| description | Text | Description | Description of the speed option \(must be unique\) | \`\` | True |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| switch | InfinibandSwitchInterface | False | one | Parent |

#### RSU

- **Description:** InfiniBand Rail-Optimized Scalable Unit
- **Label:** InfiniBand RSU
- **Icon:** mdi:network
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**identifier__value
- **Uniqueness Constraints:**identifier__value

##### Attributes

| name | kind | label | description | regex | optional |
| ---- | ---- | ----- | ----------- | ----- | -------- |
| identifier | Text | Identifier | InfiniBand RSU Identifier \(A\-Z: a unique character string\) | \[A\-Z\] |  |
| size | Number | Size | Number of InfiniBand Leaf Switches \(Rails\) in the RSU |  | True |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| switches | InfinibandSwitch | True | many | Attribute |
| interfaces | InfinibandSwitchInterface | True | many | Attribute |

#### Fabric

- **Description:** InfiniBand Network Fabric
- **Label:** InfiniBand Network Fabric
- **Icon:** mdi:network
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | label | description | unique |
| ---- | ---- | ----- | ----------- | ------ |
| name | Text | Name | InfiniBand Network Fabric Name | True |
