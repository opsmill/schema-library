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
| name | Text | False | False | 900 |  |  |  |
| disk_type | Dropdown |  | True | 950 | Specifies the type of disk | [{'name': 'ssd', 'label': 'SSD', 'description': 'Solid State Drive', 'color': '#a6c1ff'}, {'name': 'nvme', 'label': 'NVMe', 'description': 'Non-Volatile Memory Express', 'color': '#ffbf80'}, {'name': 'hdd', 'label': 'HDD', 'description': 'Hard Disk Drive', 'color': '#80c7a6'}, {'name': 'hybrid', 'label': 'Hybrid', 'description': 'Hybrid Drive', 'color': '#ffcc80'}] |  |
| status | Dropdown |  |  |  | Lifecycle status of the hardware component. | [{'name': 'in_inventory', 'label': 'In Inventory', 'description': 'The disk is newly acquired and held in inventory.', 'color': '#6c757d'}, {'name': 'active', 'label': 'Active', 'description': 'The disk is currently in use within the infrastructure.', 'color': '#28a745'}, {'name': 'decommissioned', 'label': 'Decommissioned', 'description': 'The disk is retired from active use but still stored for potential reuse or auditing.', 'color': '#17a2b8'}, {'name': 'disposed', 'label': 'Disposed', 'description': 'The disk has been securely erased and disposed of.', 'color': '#dc3545'}] |  |
| size | Number |  | False | 1000 | Disk capacity (in GB). |  | Size (GB) |
| serial_number | Text | True | True | 1100 | Serial number of the disk |  |  |
| description | Text | False | True | 1500 |  |  |  |

#### Relationships
| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| device | DcimDeviceWithPhysicalDisks | False | one | Parent | 800 |
