# Linecards

This schema extension allows you to capture Linecard related information like the version. You can insert the Linecard into a Dcim Physcial Device and leverage the Linecard type model. The Linecard can accept PIC to help configure PORT informations like breakout-capabilities and configurations.


Dependencies: `base, extensions.modules`
## Overview
- **Version:** 1.0
## Nodes
### **LinecardType**
- **Description:** Linecard Type information, detailing specifications such as part number and manufacturer.
- **Label:** Linecard Type
- **Include in Menu:** ❌
---
#### Relationships
| name | peer | cardinality | kind | description |
| ---- | ---- | ----------- | ---- | ----------- |
| linecards | InfraLinecard | many | Generic | Linecards of this type. |

### **Linecard**
- **Description:** A Linecard installed in a device, specifying slot, power status, and functionalities.
- **Label:** Linecard
- **Icon:** bi:pci-card
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** device__name__value, slot__value
- **Uniqueness Constraints:** serial_number__value
---
#### Attributes
| name | kind | description | order_weight | label | optional | default_value |
| ---- | ---- | ----------- | ------------ | ----- | -------- | ------------- |
| slot | Number | The slot number where the Linecard is installed within the device | 1050 |  |  |  |
| bng_enabled | Boolean | BNG activated or deactivated on the Linecard | 1400 | BNG Enabled | True | False |

#### Relationships
| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| linecard_type | Linecard Type | DeviceLinecardType | False | one | Attribute | 1150 |
| pics | PICs | DevicePic | True | many | Attribute | 1500 |

### **Pic**
- **Description:** Physical Interface Card (PIC) installed in the Linecard, containing multiple ports.
- **Label:** PIC
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** linecard__serial_number__value, slot__value
- **Uniqueness Constraints:** linecard + slot__value
---
#### Attributes
| name | kind | description | order_weight |
| ---- | ---- | ----------- | ------------ |
| slot | Number | Slot number of the PIC within the Linecard | 1200 |

#### Relationships
| name | label | peer | identifier | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | ---------- | -------- | ----------- | ---- | ------------ |
| linecard | Linecard | DeviceLinecard | linecard__pics | False | one | Parent | 1000 |
| ports | Ports | InfraPort |  | True | many | Component | 1100 |

### **Port**
- **Description:** A network port on a PIC, specifying speed and port number.
- **Label:** Port
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** pic__slot__value, port_number__value
- **Uniqueness Constraints:** pic + port_number__value
---
#### Attributes
| name | kind | description | order_weight | choices |
| ---- | ---- | ----------- | ------------ | ------- |
| port_number | Number | Port number on the PIC | 1100 |  |
| speed | Dropdown | Speed of the port | 1200 | [{'name': '10g', 'label': '10Gbps', 'description': '10 Gigabit per second', 'color': '#A9CCE3'}, {'name': '100g', 'label': '100Gbps', 'description': '100 Gigabit per second', 'color': '#9fbdf2'}] |

#### Relationships
| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| pic | PIC | DevicePic | False | one | Parent | 1000 |
