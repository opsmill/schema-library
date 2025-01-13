# Compute

With this schema extension in place you will be able to capture all your physical servers. It also gives you the baseline to build virtualization. You might consider HostingCluster extension to go with!


Dependencies: `base`
## Overview
- **Version:** 1.0
## Generics
### **GenericUnit**
- **Description:** A generic unit that can compute (e.g. server, vm ...).
- **Include in Menu:** ❌
---
### **HostVirtualMachine**
- **Description:** A generic unit that can host VM
- **Include in Menu:** ❌
---
#### Relationships
| name | cardinality | peer | kind | optional |
| ---- | ----------- | ---- | ---- | -------- |
| virtual_machines | many | VirtualizationVirtualMachine | Component | True |

## Nodes
### **PhysicalServer**
- **Description:** A physical server with fixed resources and specific hardware characteristics.
- **Label:** Physical Server
- **Icon:** mdi:server
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | optional | order_weight | choices |
| ---- | ---- | -------- | ------------ | ------- |
| status | Dropdown | False | 1100 | [{'name': 'active', 'label': 'Active', 'description': 'Fully operational and currently in service.', 'color': '#7fbf7f'}, {'name': 'provisioning', 'label': 'Provisioning', 'description': 'In the process of being set up and configured.', 'color': '#ffff7f'}, {'name': 'maintenance', 'label': 'Maintenance', 'description': 'Undergoing routine maintenance or repairs.', 'color': '#ffd27f'}, {'name': 'drained', 'label': 'Drained', 'description': 'Temporarily taken out of service.', 'color': '#bfbfbf'}] |

### **VirtualMachine**
- **Description:** A virtual machine hosted on a server or a cluster.
- **Label:** Virtual Machine
- **Icon:** carbon:virtual-machine
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | optional | description | order_weight | choices |
| ---- | ---- | -------- | ----------- | ------------ | ------- |
| role | Dropdown | True | Role of the virtual machine. | 1400 | [{'name': 'application', 'color': '#7f7fff'}, {'name': 'storage', 'color': '#bf7fbf'}] |
| vcpu | Number | True | Number of CPU cores assigned to the VM. | 1900 |  |
| memory | Number | True | Amount of memory (in GB) assigned to the VM. | 1900 |  |
| disk | Number | True | Disk space (in GB) assigned to the VM. | 1900 |  |

#### Relationships
| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| host | VirtualizationHostVirtualMachine | False | one | Attribute | 1500 |
