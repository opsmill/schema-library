# Cluster

This schema extension contains the foundations to capture clusters. With this one in place you can unlock various clusters flavors (hosting cluster able to host VMs, firewall clusters built with specific appliances ...)


Dependencies: `base, extensions.compute`
## Overview
- **Version:** 1.0
## Generics
### **Generic**
- **Description:** A cluster of machines hosting services or other machines.
- **Label:** Clusters
- **Icon:** mdi:dots-hexagon
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | description | unique | order_weight | optional |
| ---- | ---- | ----------- | ------ | ------------ | -------- |
| name | Text | Name of the cluster. | True | 1000 |  |
| description | Text |  |  |  | True |

#### Relationships
| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| location | Location | LocationGeneric | False | many | Attribute | 1400 |
| tags |  | BuiltinTag | True | many | Attribute | 2000 |

### **GenericComputeUnitNodes**
- **Description:** A generic to apply on clusters that can be built out of generic compute units.
- **Include in Menu:** ❌
---
#### Relationships
| name | label | identifier | cardinality | peer | kind |
| ---- | ----- | ---------- | ----------- | ---- | ---- |
| nodes | Nodes | worker_in_cluster | many | ComputeGenericUnit | Component |

## Extensions
### ComputeGenericUnit
#### Attributes
|  |
|  |

#### Relationships
| name | identifier | label | peer | cardinality | description | optional |
| ---- | ---------- | ----- | ---- | ----------- | ----------- | -------- |
| worker_in_cluster | worker_in_cluster | Worker in cluster | ClusterGenericComputeUnitNodes | one | This device is a worker node of the specified cluster. | True |

### LocationGeneric
#### Attributes
|  |
|  |

#### Relationships
| name | label | peer | cardinality | kind | description | optional |
| ---- | ----- | ---- | ----------- | ---- | ----------- | -------- |
| clusters | Clusters | ClusterGeneric | many | Component | All clusters available on that location. | True |
