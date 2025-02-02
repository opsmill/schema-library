# Routing Engine

This schema extension allows you to capture Routing Engine related information like the version. You can insert the Routing Engine into a Dcim Physical Device and leverage the Routing Engine type model.

Dependencies: `base, extensions.modules`

## Overview

- **Version:** 1.0

## Nodes

### RoutingEngineType

- **Description:** Routing Engine Type information, detailing specifications such as part number and manufacturer.
- **Label:** Routing Engine Type
- **Include in Menu:** ❌

#### Relationships

| name | peer | cardinality | kind | description |
| ---- | ---- | ----------- | ---- | ----------- |
| routing\_engines | InfraRoutingEngine | many | Generic | Routing engines of this type\. |

### RoutingEngine

- **Description:** A Routing Engine (RE) installed in a device, responsible for routing functionalities.
- **Label:** Routing Engine
- **Icon:** mdi:cpu-64-bit
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**device__name__value, slot__value
- **Uniqueness Constraints:**serial_number__value

#### Attributes

| name | kind | description | order_weight | label | optional |
| ---- | ---- | ----------- | ------------ | ----- | -------- |
| slot | Number | The slot number where the Routing Engine is installed within the device | 1100 |  |  |
| version | Text | Firmware version of the Routing Engine\. | 1200 | Version | True |

#### Relationships

| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| routing\_engine\_type | RE Type | InfraRoutingEngineType | False | one | Attribute | 1150 |
