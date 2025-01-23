# Hosting Cluster

A rather generic cluster built with compute units (e.g. servers) and able to host VMs.

Dependencies: `base, extensions.cluster, extensions.compute`

## Overview

- **Version:** 1.0

## Nodes

### Hosting

- **Description:** A cluster hosting virtual machines.
- **Label:** Hosting Cluster
- **Icon:** mdi:dots-hexagon
- **Menu Placement:** ClusterGeneric
- **Include in Menu:** ❌

#### Attributes

| name | kind | order_weight | description | choices | optional |
| ---- | ---- | ------------ | ----------- | ------- | -------- |
| cluster_type | Dropdown | 1200 | Type of the cluster. | `aws, kvm, gcp, vmware` |  |
| status | Dropdown | 1300 |  | `active, provisioning, maintenance, drained` | False |
