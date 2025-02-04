# Compute

With this schema extension in place you will be able to capture all your physical servers. It also gives you the baseline to build virtualization. You might consider HostingCluster extension to go with!

Dependencies: `base`

## compute

- **Version:** 1.0

## Generics

### GenericUnit

- **Description:** A generic unit that can compute (e.g. server, vm ...).
- **Include in Menu:** ❌

### HostVirtualMachine

- **Description:** A generic unit that can host VM
- **Include in Menu:** ❌

#### Relationships

| name | cardinality | peer | kind | optional |
| ---- | ----------- | ---- | ---- | -------- |
| virtual\_machines | many | VirtualizationVirtualMachine | Component | True |

## Nodes

### PhysicalServer

- **Description:** A physical server with fixed resources and specific hardware characteristics.
- **Label:** Physical Server
- **Icon:** mdi:server
- **Include in Menu:** ❌

#### Attributes

| name | kind | optional | order_weight | choices |
| ---- | ---- | -------- | ------------ | ------- |
| status | Dropdown | False | 1100 | \`active, provisioning, maintenance, drained\` |

### VirtualMachine

- **Description:** A virtual machine hosted on a server or a cluster.
- **Label:** Virtual Machine
- **Icon:** carbon:virtual-machine
- **Include in Menu:** ❌

#### Attributes

| name | kind | optional | description | order_weight | choices |
| ---- | ---- | -------- | ----------- | ------------ | ------- |
| role | Dropdown | True | Role of the virtual machine\. | 1400 | \`application, storage\` |
| vcpu | Number | True | Number of CPU cores assigned to the VM\. | 1900 | \`\` |
| memory | Number | True | Amount of memory \(in GB\) assigned to the VM\. | 1900 | \`\` |
| disk | Number | True | Disk space \(in GB\) assigned to the VM\. | 1900 | \`\` |

#### Relationships

| name | peer | optional | cardinality | kind | order_weight |
| ---- | ---- | -------- | ----------- | ---- | ------------ |
| host | VirtualizationHostVirtualMachine | False | one | Attribute | 1500 |
