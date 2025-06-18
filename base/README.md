## Base Schemas

The base schemas serve as the foundation for every single schema extension you might want to use afterward. This one is mandatory and will unlock access to the extensions section.

- **Version:** 1.0

### Generics

#### GenericDevice

- **Description:** Generic Device object.
- **Label:** Device
- **Icon:** mdi:server
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 2000 | True |
| os\_version | Text |  | 2200 | True |

#### Relationships

| name | peer | optional | cardinality | identifier | kind | order_weight | label |
| ---- | ---- | -------- | ----------- | ---------- | ---- | ------------ | ----- |
| interfaces | DcimInterface | True | many | device\_\_interface | Component |  |  |
| tags | BuiltinTag | True | many |  | Attribute | 2000 |  |
| primary\_address | IpamIPAddress | True | one |  | Attribute | 1700 | Primary IP Address |
| platform | DcimPlatform | True | one |  | Attribute | 1250 |  |

#### PhysicalDevice

- **Description:** Generic holding attributes and relationships relevant for physical device.
- **Include in Menu:** ❌

##### Attributes

| name | label | description | kind | optional | order_weight | default_value | choices |
| ---- | ----- | ----------- | ---- | -------- | ------------ | ------------- | ------- |
| position | Position \(U\) | Lowest unit\. | Number | True | 1500 |  | \`\` |
| serial |  |  | Text | True | 1500 |  | \`\` |
| rack\_face | Rack Face | On which face of the rack the device is mounted\. | Dropdown | False | 1515 | front | \`front, rear\` |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight | label |
| ---- | ---- | -------- | ----------- | ---- | ------------ | ----- |
| device\_type | DcimDeviceType | True | one | Attribute | 1200 |  |
| location | LocationHosting | False | one | Attribute | 1500 | Location |

#### Endpoint

- **Description:** Generic Endpoint to receive a connector.
- **Include in Menu:** ❌

#### Relationships

| name | peer | optional | cardinality | order_weight | kind |
| ---- | ---- | -------- | ----------- | ------------ | ---- |
| connector | DcimConnector | True | one | 1500 | Attribute |

#### Connector

- **Description:** Generic Connector to link two endpoints together.
- **Include in Menu:** ❌

#### Relationships

| name | peer | optional | cardinality | order_weight | kind |
| ---- | ---- | -------- | ----------- | ------------ | ---- |
| connected\_endpoints | DcimEndpoint | True | many | 1500 | Generic |

#### Interface

- **Description:** Generic Network Interface
- **Label:** Interface
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**device__name__value, name__value
- **Uniqueness Constraints:**device + name__value

##### Attributes

| name | kind | description | order_weight | optional | label | default_value | choices |
| ---- | ---- | ----------- | ------------ | -------- | ----- | ------------- | ------- |
| name | Text | Name of the interface | 1000 |  |  |  | \`\` |
| description | Text | A brief description of the interface | 1100 | True |  |  | \`\` |
| mtu | Number |  | 1300 |  | MTU | 1514 | \`\` |
| status | Dropdown | The status of the interface | 1200 |  |  | active | \`provisioning, free, active, maintenance, disabled, deleted, outage\` |
| role | Dropdown | The role of the interface in the network | 1250 | True |  |  | \`lag, core, cust, access, management, peering, upstream\` |

#### Relationships

| name | peer | identifier | optional | cardinality | kind | order_weight |
| ---- | ---- | ---------- | -------- | ----------- | ---- | ------------ |
| device | DcimGenericDevice | device\_\_interface | False | one | Parent | 1025 |
| tags | BuiltinTag |  | True | many | Attribute | 3000 |

#### Layer2

- **Description:** Layer 2 specific attributes for network interfaces
- **Label:** Layer 2 Interface
- **Include in Menu:** ❌

##### Attributes

| name | label | kind | optional | choices | description | order_weight |
| ---- | ----- | ---- | -------- | ------- | ----------- | ------------ |
| l2\_mode | Layer2 Mode | Dropdown | True | \`access, trunk, trunk\_all\` | Layer 2 mode of the interface | 1500 |

#### Layer3

- **Description:** Layer 3 specific attributes for network interfaces
- **Label:** Layer 3 Interface
- **Include in Menu:** ❌

##### Attributes

| name | label | kind | description | order_weight | optional |
| ---- | ----- | ---- | ----------- | ------------ | -------- |
| dot1q\_id | VLAN ID \(dot1q\) | Number | Dot1Q VLAN ID | 1600 | True |
| mac\_address | Mac Address | Text |  | 1550 | True |

#### Relationships

| name | label | peer | cardinality | kind | optional | description | order_weight |
| ---- | ----- | ---- | ----------- | ---- | -------- | ----------- | ------------ |
| ip\_addresses | IP Addresses | IpamIPAddress | many | Attribute | True | List of IP addresses associated with the interface | 1150 |

#### HasSubInterface

- **Description:** A generic interface that can have sub-interfaces
- **Include in Menu:** ❌

#### Relationships

| name | label | peer | identifier | optional | cardinality | kind | description | order_weight |
| ---- | ----- | ---- | ---------- | -------- | ----------- | ---- | ----------- | ------------ |
| sub\_interfaces | Sub\-interface\(s\) | InterfaceVirtual | sub\_\_interface | True | many | Attribute | Sub\-interfaces of this interface | 1750 |

### Nodes

#### DeviceType

- **Description:** A model of device
- **Label:** Device Type
- **Icon:** mdi:poll
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**manufacturer__name__value, name__value
- **Uniqueness Constraints:**manufacturer + name__value

##### Attributes

| name | kind | unique | order_weight | optional | label | default_value |
| ---- | ---- | ------ | ------------ | -------- | ----- | ------------- |
| name | Text | True | 1000 |  |  |  |
| description | Text |  | 1100 | True |  |  |
| part\_number | Text |  | 1200 | True | Part Number |  |
| height | Number |  | 1400 | False | Height \(U\) | 1 |
| full\_depth | Boolean |  | 1500 |  | Full Depth | True |
| weight | Number |  | 1600 | True | Weight \(kg\) |  |

#### Relationships

| name | peer | cardinality | kind | order_weight | optional |
| ---- | ---- | ----------- | ---- | ------------ | -------- |
| platform | DcimPlatform | one | Attribute | 1300 |  |
| manufacturer | OrganizationManufacturer | one | Attribute | 1250 | False |
| tags | BuiltinTag | many | Attribute | 2000 | True |

#### Platform

- **Description:** A Platform represent the type of software running on a device.
- **Label:** Platform
- **Icon:** mdi:application-cog-outline
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**manufacturer__name__value, name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 1200 | True |
| nornir\_platform | Text |  | 1500 | True |
| napalm\_driver | Text |  | 1600 | True |
| netmiko\_device\_type | Text |  | 1700 | True |
| ansible\_network\_os | Text |  | 1800 | True |
| containerlab\_os | Text |  | 1900 | True |

#### Relationships

| name | peer | optional | cardinality | order_weight | kind |
| ---- | ---- | -------- | ----------- | ------------ | ---- |
| devices | DcimGenericDevice | True | many | 1350 |  |
| manufacturer | OrganizationManufacturer |  | one | 1300 | Attribute |

#### Device

- **Description:** A configurable network device for managing and directing data traffic, including routers, switches...
- **Label:** Network Device
- **Icon:** clarity:network-switch-solid
- **Include in Menu:** ❌

##### Attributes

| name | kind | optional | order_weight | choices |
| ---- | ---- | -------- | ------------ | ------- |
| status | Dropdown | False | 1100 | \`active, provisioning, maintenance, drained\` |
| role | Dropdown | True | 1400 | \`core, edge, cpe, spine, leaf, tor\` |

#### Physical

- **Description:** Physical network port on a device
- **Label:** Physical Interface
- **Include in Menu:** ❌

#### Virtual

- **Description:** Virtual interface like VLAN or Loopback
- **Label:** Virtual Interface
- **Include in Menu:** ❌

#### Relationships

| name | peer | cardinality | kind | identifier | description |
| ---- | ---- | ----------- | ---- | ---------- | ----------- |
| parent\_interface | InterfaceHasSubInterface | one | Attribute | sub\_\_interface | Parent interface to which this sub\-interface belongs |

- **Version:** 1.0

### Generics

#### Generic

- **Description:** An organization represent a legal entity, a company.
- **Label:** Organization
- **Icon:** mdi:domain
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 1200 | True |

#### Relationships

| name | peer | cardinality | kind | optional | order_weight |
| ---- | ---- | ----------- | ---- | -------- | ------------ |
| tags | BuiltinTag | many | Attribute | True | 3000 |

### Nodes

#### Manufacturer

- **Description:** Device Manufacturer
- **Icon:** mdi:domain
- **Menu Placement:** OrganizationGeneric
- **Include in Menu:** ✅

#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| device\_type | DcimDeviceType | many | True |
| platform | DcimPlatform | many | True |

#### Provider

- **Description:** Circuit or Location Provider
- **Icon:** mdi:domain
- **Menu Placement:** OrganizationGeneric
- **Include in Menu:** ✅

- **Version:** 1.0

### Generics

#### Generic

- **Description:** Generic Location, could be a country, city ...
- **Label:** Location
- **Icon:** mingcute:location-line
- **Include in Menu:** ✅

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

##### Attributes

| name | kind | order_weight | unique | optional |
| ---- | ---- | ------------ | ------ | -------- |
| name | Text | 1000 |  |  |
| shortname | Text | 1100 | True |  |
| description | Text | 1200 |  | True |

#### Relationships

| name | peer | kind | optional | cardinality |
| ---- | ---- | ---- | -------- | ----------- |
| tags | BuiltinTag | Attribute | True | many |

#### Hosting

- **Description:** Location directly hosting device and services.
- **Include in Menu:** ❌

#### Relationships

| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| prefixes | Prefixes | IpamPrefix | many | True |
| devices | Devices | DcimPhysicalDevice | many | True |

- **Version:** 1.0

### Nodes

#### IPAddress

- **Description:** IP Address
- **Label:** IP Address
- **Icon:** mdi:ip
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**address__value
- **Uniqueness Constraints:**ip_namespace + address__value

##### Attributes

| name | label | kind | optional | regex |
| ---- | ----- | ---- | -------- | ----- |
| fqdn | FQDN | Text | True | \(?=^\.{1,253}\$\)\(^\(\(\(?\!\-\)\[a\-zA\-Z0\-9\-\]{1,63}\(?\<\!\-\)\)\|\(\(?\!\-\)\[a\-zA\-Z0\-9\-\]{1,63}\(?\<\!\-\)\\.\)\+\[a\-zA\-Z\]{2,63}\)\$\) |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| interface | InterfaceLayer3 | True | one |

#### Prefix

- **Description:** IPv4 or IPv6 network (with mask)
- **Label:** Prefix
- **Icon:** mdi:ip-network
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**prefix__value
- **Uniqueness Constraints:**ip_namespace + prefix__value

##### Attributes

| name | kind | choices | optional |
| ---- | ---- | ------- | -------- |
| status | Dropdown | \`active, deprecated, reserved\` |  |
| role | Dropdown | \`loopback, management, public, server, supernet, technical, loopback\-vtep\` | True |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight | label | identifier |
| ---- | ---- | -------- | ----------- | ---- | ------------ | ----- | ---------- |
| organization | OrganizationGeneric | True | one | Attribute | 1200 |  |  |
| location | LocationHosting | True | one | Attribute | 1300 |  |  |
| gateway | IpamIPAddress | True | one | Attribute | 1500 | L3 Gateway | prefix\_\_gateway |
