# Base Schemas

That's the foundation for every single schema extension you might want to use afterward. This one is mandatory and will unlock access to the extensions section.

## Overview

- **Version:** 1.0

## Generics

### GenericDevice

- **Description:** Generic Device object.
- **Label:** Device
- **Icon:** mdi:server
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
#### Attributes

| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 2000 | True |
| os_version | Text |  | 2200 | True |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight | label |
| ---- | ---- | -------- | ----------- | ---- | ------------ | ----- |
| interfaces | DcimInterface | True | many | Component |  |  |
| tags | BuiltinTag | True | many | Attribute | 2000 |  |
| primary_address | IpamIPAddress | True | one | Attribute | 1700 | Primary IP Address |
| platform | DcimPlatform | True | one | Attribute | 1250 |  |

### PhysicalDevice

- **Description:** Generic holding attributes and relationships relevant for physical device.
- **Include in Menu:** ❌

#### Attributes

| name | label | description | kind | optional | order_weight | default_value | choices |
| ---- | ----- | ----------- | ---- | -------- | ------------ | ------------- | ------- |
| position | Position (U) | Lowest unit. | Number | True | 1500 |  | `` |
| serial |  |  | Text | True | 1500 |  | `` |
| rack_face | Rack Face | On which face of the rack the device is mounted. | Dropdown | False | 1515 | front | `front, rear` |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight | label |
| ---- | ---- | -------- | ----------- | ---- | ------------ | ----- |
| device_type | DcimDeviceType | True | one | Attribute | 1200 |  |
| location | LocationHosting | False | one | Attribute | 1500 | Location |

### Interface

- **Description:** Generic Network Interface.
- **Label:** Interface
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimGenericDevice
- **Include in Menu:** ✅


#### Ordering and Constraints
- **Order By:** device__name__value, name__value
- **Uniqueness Constraints:** device + name__value
#### Attributes

| name | kind | order_weight | optional | label | default_value |
| ---- | ---- | ------------ | -------- | ----- | ------------- |
| name | Text | 1000 |  |  |  |
| description | Text | 1100 | True |  |  |
| speed | Number | 1400 |  |  |  |
| mtu | Number | 1500 |  | MTU | 1500 |
| enabled | Boolean | 1200 |  |  | True |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| device | DcimGenericDevice | False | one | Parent |
| tags | BuiltinTag | True | many | Attribute |

### Endpoint

- **Description:** Generic Endpoint to receive a connector.
- **Include in Menu:** ❌

#### Relationships

| name | peer | optional | cardinality | order_weight | kind |
| ---- | ---- | -------- | ----------- | ------------ | ---- |
| connector | DcimConnector | True | one | 1500 | Attribute |

### Connector

- **Description:** Generic Connector to link two endpoints together.
- **Include in Menu:** ❌

#### Relationships

| name | peer | optional | cardinality | order_weight | kind |
| ---- | ---- | -------- | ----------- | ------------ | ---- |
| connected_endpoints | DcimEndpoint | True | many | 1500 | Generic |

## Nodes

### DeviceType

- **Description:** A model of device
- **Label:** Device Type
- **Icon:** mdi:poll
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** manufacturer__name__value, name__value
- **Uniqueness Constraints:** manufacturer + name__value
#### Attributes

| name | kind | unique | order_weight | optional | label | default_value |
| ---- | ---- | ------ | ------------ | -------- | ----- | ------------- |
| name | Text | True | 1000 |  |  |  |
| description | Text |  | 1100 | True |  |  |
| part_number | Text |  | 1200 | True | Part Number |  |
| height | Number |  | 1400 | False | Height (U) | 1 |
| full_depth | Boolean |  | 1500 |  | Full Depth | True |
| weight | Number |  | 1600 | True | Weight (kg) |  |

#### Relationships

| name | peer | cardinality | kind | order_weight | optional |
| ---- | ---- | ----------- | ---- | ------------ | -------- |
| platform | DcimPlatform | one | Attribute | 1300 |  |
| manufacturer | OrganizationManufacturer | one | Attribute | 1250 | False |
| tags | BuiltinTag | many | Attribute | 2000 | True |

### Platform

- **Description:** A Platform represent the type of software running on a device.
- **Label:** Platform
- **Icon:** mdi:application-cog-outline
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** manufacturer__name__value, name__value
- **Uniqueness Constraints:** name__value
#### Attributes

| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 1200 | True |
| nornir_platform | Text |  | 1500 | True |
| napalm_driver | Text |  | 1600 | True |
| netmiko_device_type | Text |  | 1700 | True |
| ansible_network_os | Text |  | 1800 | True |
| containerlab_os | Text |  | 1900 | True |

#### Relationships

| name | peer | optional | cardinality | order_weight | kind |
| ---- | ---- | -------- | ----------- | ------------ | ---- |
| devices | DcimGenericDevice | True | many | 1350 |  |
| manufacturer | OrganizationManufacturer |  | one | 1300 | Attribute |

### Device

- **Description:** A configurable network device for managing and directing data traffic, including routers, switches...
- **Label:** Network Device
- **Icon:** clarity:network-switch-solid
- **Include in Menu:** ❌

#### Attributes

| name | kind | optional | order_weight | choices |
| ---- | ---- | -------- | ------------ | ------- |
| status | Dropdown | False | 1100 | `active, provisioning, maintenance, drained` |
| role | Dropdown | True | 1400 | `core, edge, cpe, spine, leaf, tor` |

### InterfaceL3

- **Description:** Network Layer 3 Interface
- **Label:** Interface L3
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimInterface
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
#### Attributes

| name | kind | optional | choices | order_weight |
| ---- | ---- | -------- | ------- | ------------ |
| role | Dropdown | True | `backbone, upstream, peering, peer, server, loopback, management, uplink, leaf, spare` | 1700 |
| status | Dropdown | True | `active, provisioning, maintenance, drained` | 1300 |

#### Relationships

| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| ip_addresses | IpamIPAddress | True | many | Component |

### InterfaceL2

- **Description:** Network Layer 2 Interface
- **Label:** Interface L2
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimInterface
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
#### Attributes

| name | kind | optional | choices | order_weight | label | enum |
| ---- | ---- | -------- | ------- | ------------ | ----- | ---- |
| role | Dropdown | True | `backbone, upstream, peering, peer, server, loopback, management, uplink, leaf, spare` | 1700 |  |  |
| status | Dropdown | True | `active, provisioning, maintenance, drained` | 1300 |  |  |
| l2_mode | Text |  | `` | 1250 | Layer2 Mode | ['Access', 'Trunk', 'Tunnel'] |

## Overview

- **Version:** 1.0

## Generics

### Generic

- **Description:** An organization represent a legal entity, a company.
- **Label:** Organization
- **Icon:** mdi:domain
- **Include in Menu:** ✅


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
#### Attributes

| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 1200 | True |

#### Relationships

| name | peer | cardinality | kind | optional | order_weight |
| ---- | ---- | ----------- | ---- | -------- | ------------ |
| tags | BuiltinTag | many | Attribute | True | 3000 |

## Nodes

### Manufacturer

- **Description:** Device Manufacturer
- **Icon:** mdi:domain
- **Menu Placement:** OrganizationGeneric
- **Include in Menu:** ✅

#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| device_type | DcimDeviceType | many | True |
| platform | DcimPlatform | many | True |

### Provider

- **Description:** Circuit or Location Provider
- **Icon:** mdi:domain
- **Menu Placement:** OrganizationGeneric
- **Include in Menu:** ✅

## Overview

- **Version:** 1.0

## Generics

### Generic

- **Description:** Generic Location, could be a country, city ...
- **Label:** Location
- **Icon:** mingcute:location-line
- **Include in Menu:** ✅


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
#### Attributes

| name | kind | order_weight | unique | optional |
| ---- | ---- | ------------ | ------ | -------- |
| name | Text | 1000 |  |  |
| shortname | Text | 1100 | True |  |
| description | Text | 1200 |  | True |

#### Relationships

| name | peer | kind | optional | cardinality |
| ---- | ---- | ---- | -------- | ----------- |
| tags | BuiltinTag | Attribute | True | many |

### Hosting

- **Description:** Location directly hosting device and services.
- **Include in Menu:** ❌

#### Relationships

| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| prefixes | Prefixes | IpamPrefix | many | True |
| devices | Devices | DcimPhysicalDevice | many | True |

## Overview

- **Version:** 1.0

## Nodes

### IPAddress

- **Description:** IP Address
- **Label:** IP Address
- **Icon:** mdi:ip
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** address__value
- **Uniqueness Constraints:** ip_namespace + address__value
#### Attributes

| name | label | kind | optional | regex |
| ---- | ----- | ---- | -------- | ----- |
| fqdn | FQDN | Text | True | (?=^.{1,253}$)(^(((?!-)[a-zA-Z0-9-]{1,63}(?<!-))|((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63})$) |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| interface | DcimInterfaceL3 | True | one |

### Prefix

- **Description:** IPv4 or IPv6 network (with mask)
- **Label:** Prefix
- **Icon:** mdi:ip-network
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** prefix__value
- **Uniqueness Constraints:** ip_namespace + prefix__value
#### Attributes

| name | kind | choices | optional |
| ---- | ---- | ------- | -------- |
| status | Dropdown | `active, deprecated, reserved` |  |
| role | Dropdown | `loopback, management, public, server, supernet, technical, loopback-vtep` | True |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight | label | identifier |
| ---- | ---- | -------- | ----------- | ---- | ------------ | ----- | ---------- |
| organization | OrganizationGeneric | True | one | Attribute | 1200 |  |  |
| location | LocationHosting | True | one | Attribute | 1300 |  |  |
| gateway | IpamIPAddress | True | one | Attribute | 1500 | L3 Gateway | prefix__gateway |
