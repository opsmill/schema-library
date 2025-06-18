# Linecard Module

This schema extension allows you to capture Linecard related information like the version. You can insert the Linecard into a Dcim Physical Device and leverage the Linecard type model. The Linecard can accept PIC to help configure PORT information like breakout-capabilities and configurations.

Dependencies: `base, extensions/modules`

## linecard

- **Version:** 1.0

### Nodes

### LinecardType

- **Description:** Linecard Type information, detailing specifications such as part number and manufacturer.
- **Label:** Linecard Type
- **Include in Menu:** ❌

#### Relationships

| name | peer | cardinality | kind | description |
| ---- | ---- | ----------- | ---- | ----------- |
| linecards | DeviceLinecard | many | Generic | Linecards of this type\. |

### Linecard

- **Description:** A Linecard installed in a device, specifying slot, power status, and functionalities.
- **Label:** Linecard
- **Icon:** bi:pci-card
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**device__name__value, slot__value
- **Uniqueness Constraints:**serial_number__value

#### Attributes

| name | kind | description | order_weight | label | optional | default_value |
| ---- | ---- | ----------- | ------------ | ----- | -------- | ------------- |
| slot | Number | The slot number where the Linecard is installed within the device | 1050 |  |  |  |
| bng\_enabled | Boolean | BNG activated or deactivated on the Linecard | 1400 | BNG Enabled | True | False |

#### Relationships

| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| linecard\_type | Linecard Type | DeviceLinecardType | False | one | Attribute | 1150 |
| pics | PICs | DevicePic | True | many | Attribute | 1500 |

### Pic

- **Description:** Physical Interface Card (PIC) installed in the Linecard, containing multiple ports.
- **Label:** PIC
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**linecard__serial_number__value, slot__value
- **Uniqueness Constraints:**linecard + slot__value

#### Attributes

| name | kind | description | order_weight |
| ---- | ---- | ----------- | ------------ |
| slot | Number | Slot number of the PIC within the Linecard | 1200 |

#### Relationships

| name | label | peer | identifier | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | ---------- | -------- | ----------- | ---- | ------------ |
| linecard | Linecard | DeviceLinecard | linecard\_\_pics | False | one | Parent | 1000 |
| ports | Ports | InfraPort |  | True | many | Component | 1100 |

### Port

- **Description:** A network port on a PIC, specifying speed and port number.
- **Label:** Port
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**pic__slot__value, port_number__value
- **Uniqueness Constraints:**pic + port_number__value

#### Attributes

| name | kind | description | order_weight | choices |
| ---- | ---- | ----------- | ------------ | ------- |
| port\_number | Number | Port number on the PIC | 1100 | \`\` |
| speed | Dropdown | Speed of the port | 1200 | \`10g, 100g\` |

#### Relationships

| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| pic | PIC | DevicePic | False | one | Parent | 1000 |
