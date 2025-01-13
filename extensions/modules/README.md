# Modules

This schema extension allows you to capture Device Modules related information like the serial number or the satus. You can insert the Module into a Dcim Physcial Device.

> [!NOTE]
> This extension doesn't contain any Node, you can use the extension module_linecards or modules_routing_engine to use it



Dependencies: `base`
## Overview
- **Version:** 1.0
## Generics
### **GenericModule**
- **Description:** A generic module, such as a Linecard or Routing Engine, installed in a device.
- **Label:** Module
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | unique | description | order_weight | optional | choices | default_value |
| ---- | ---- | ------ | ----------- | ------------ | -------- | ------- | ------------- |
| serial_number | Text | True | Unique serial number of the module. | 1000 |  |  |  |
| description | Text |  |  | 1100 | True |  |  |
| status | Dropdown |  |  | 1300 |  | [{'name': 'provisioning', 'label': 'Provisioning', 'description': 'Linecard is being provisioned.', 'color': '#A9DFBF'}, {'name': 'active', 'label': 'Active', 'description': 'Linecard is active and operational.', 'color': '#A9CCE3'}, {'name': 'maintenance', 'label': 'Maintenance', 'description': 'Linecard is under maintenance.', 'color': '#FFF2CC'}, {'name': 'disabled', 'label': 'Disabled', 'description': 'Linecard has been disabled.', 'color': '#D3D3D3'}, {'name': 'outage', 'label': 'Outage', 'description': 'Linecard is currently experiencing an outage.', 'color': '#F4CCCC'}] | active |

#### Relationships
| name | peer | optional | cardinality | kind | order_weight | label | identifier |
| ---- | ---- | -------- | ----------- | ---- | ------------ | ----- | ---------- |
| module_type | DeviceGenericModuleType | False | one | Attribute | 1150 |  |  |
| device | DcimPhysicalDevice | True | one | Attribute | 1000 | Device | device__modules |

### **GenericModuleType**
- **Description:** A generic module type, with common specifications like part number and manufacturer.
- **Label:** Module Type
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** manufacturer__name__value, name__value
- **Uniqueness Constraints:** part_number__value, name__value + manufacturer
---
#### Attributes
| name | kind | unique | description | order_weight | optional | label |
| ---- | ---- | ------ | ----------- | ------------ | -------- | ----- |
| name | Text | True | Name of the module type. | 1000 |  |  |
| description | Text |  | Description of the module type. | 1100 | True |  |
| part_number | Text |  | Part number of the module. | 1200 | True | Part Number |

#### Relationships
| name | peer | identifier | cardinality | optional | kind | description | order_weight |
| ---- | ---- | ---------- | ----------- | -------- | ---- | ----------- | ------------ |
| manufacturer | OrganizationManufacturer | manufacturer__moduletype | one | False | Attribute | Manufacturer of the module type. | 1250 |
| tags | BuiltinTag |  | many | True | Attribute | Tags associated with the module type. | 3000 |

## Extensions
### DcimPhysicalDevice
#### Relationships
| name | peer | identifier | cardinality | kind |
| ---- | ---- | ---------- | ----------- | ---- |
| modules | DeviceGenericModule | device__modules | many | Component |
