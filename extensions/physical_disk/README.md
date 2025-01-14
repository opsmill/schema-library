# Physical Disks

Simple schema allowing you to capture physical disks information for the sake of inventory and lifecycle management.

> [!NOTE]
> This extension is compatible with all sort of device. You can apply the generic "DeviceWithPhysicalDisks" to particular model to enable disks tracking. You might also link that schema to location for instance to capture spares.



Dependencies: `base`
## Overview
- **Version:** 1.0
## Generics
### **DeviceWithPhysicalDisks**
- **Description:** Generic that hold relationship toward physical disks. To apply on device that can have physical disks.
- **Include in Menu:** ❌
---
#### Relationships
| name | cardinality | peer | optional | kind |
| ---- | ----------- | ---- | -------- | ---- |
| physical_disks | many | DcimPhysicalDisk | True | Component |

## Nodes
### **PhysicalDisk**
- **Description:** Physical Disk
- **Label:** Physical Disk
- **Icon:** carbon:vmdk-disk
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value + device
---
#### Attributes
| name | kind | unique | optional | order_weight | description | choices | label |
| ---- | ---- | ------ | -------- | ------------ | ----------- | ------- | ----- |
| name | Text | False | False | 900 |  | `` |  |
| disk_type | Dropdown |  | True | 950 | Specifies the type of disk | `ssd, nvme, hdd, hybrid` |  |
| status | Dropdown |  |  |  | Lifecycle status of the hardware component. | `in_inventory, active, decommissioned, disposed` |  |
| size | Number |  | False | 1000 | Disk capacity (in GB). | `` | Size (GB) |
| serial_number | Text | True | True | 1100 | Serial number of the disk | `` |  |
| description | Text | False | True | 1500 |  | `` |  |

#### Relationships
| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| device | DcimDeviceWithPhysicalDisks | False | one | Parent | 800 |
