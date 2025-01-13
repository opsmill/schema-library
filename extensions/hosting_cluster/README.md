# Hosting Cluster

A rather generic cluster built with compute units (e.g. servers) and able to host VMs.


Dependencies: `base, extensions.cluster, extensions.compute`
## Overview
- **Version:** 1.0
## Nodes
### **Hosting**
- **Description:** A cluster hosting virtual machines.
- **Label:** Hosting Cluster
- **Icon:** mdi:dots-hexagon
- **Menu Placement:** ClusterGeneric
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | order_weight | description | choices | optional |
| ---- | ---- | ------------ | ----------- | ------- | -------- |
| cluster_type | Dropdown | 1200 | Type of the cluster. | [{'name': 'aws', 'label': 'Amazon Web Service', 'color': '#b90028'}, {'name': 'kvm', 'label': 'KVM', 'color': '#0082e2'}, {'name': 'gcp', 'label': 'Google Cloud Platform', 'color': '#e29200'}, {'name': 'vmware', 'label': 'VMware', 'color': '#3d8600'}] |  |
| status | Dropdown | 1300 |  | [{'name': 'active', 'label': 'Active', 'description': 'Fully operational and currently in service.', 'color': '#7fbf7f'}, {'name': 'provisioning', 'label': 'Provisioning', 'description': 'In the process of being set up and configured.', 'color': '#ffff7f'}, {'name': 'maintenance', 'label': 'Maintenance', 'description': 'Undergoing routine maintenance or repairs.', 'color': '#ffd27f'}, {'name': 'drained', 'label': 'Drained', 'description': 'Temporarily taken out of service.', 'color': '#bfbfbf'}] | False |
