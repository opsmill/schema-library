# Topology

A schema for defining and managing network topology, strategies, and services.


Dependencies: `base`
## Overview
- **Version:** 1.0
## Generics
### **ManagementServer**
- **Description:** Generic model for network management server (dns, ntp, and dhcp).
- **Label:** Network Management Servers
- **Include in Menu:** ✅

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | order_weight | optional | choices |
| ---- | ---- | ------------ | -------- | ------- |
| name | Text | 1000 |  |  |
| description | Text | 1100 | True |  |
| status | Dropdown |  |  | [{'name': 'active', 'label': 'Active', 'description': 'Fully operational and currently in service.', 'color': '#7fbf7f'}, {'name': 'provisioning', 'label': 'Provisioning', 'description': 'In the process of being set up and configured.', 'color': '#ffff7f'}, {'name': 'maintenance', 'label': 'Maintenance', 'description': 'Undergoing routine maintenance or repairs.', 'color': '#ffd27f'}, {'name': 'drained', 'label': 'Drained', 'description': 'Temporarily taken out of service.', 'color': '#bfbfbf'}] |

#### Relationships
| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| location | LocationGeneric | True | many |  |
| ip_addresses | InfraIPAddress | True | many | Component |

### **GenericElement**
- **Description:** Base model for elements
- **Label:** Generic Topology Element
- **Icon:** carbon:network-3-reference
- **Menu Placement:** TopologyTopology
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| name | Text | 1000 |  |
| description | Text | 1100 | True |
| quantity | Number | 1200 |  |

#### Relationships
| name | peer | cardinality | kind | optional |
| ---- | ---- | ----------- | ---- | -------- |
| topology | TopologyTopology | one | Parent | False |

### **NetworkStrategy**
- **Description:** Generic model for network strategies (underlays and overlays).
- **Label:** Network Strategy
- **Icon:** iconoir:strategy
- **Menu Placement:** TopologyTopology
- **Include in Menu:** ✅

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| name | Text | 1000 |  |
| description | Text | 1100 | True |

#### Relationships
| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| topology | TopologyTopology | True | many |

## Nodes
### **Topology**
- **Description:** A Topology represents the entire network pod.
- **Label:** Topology
- **Icon:** carbon:network-3
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | unique | order_weight | optional |
| ---- | ---- | ------ | ------------ | -------- |
| name | Text | True | 1000 |  |
| description | Text |  | 1100 | True |

#### Relationships
| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| elements | TopologyGenericElement | True | many | Component |
| strategy | TopologyNetworkStrategy | True | one | Component |
| location | LocationGeneric | True | one | Attribute |
| devices | DcimGenericDevice | True | many | Component |
| network_services | TopologyNetworkService | True | many | Component |

### **MPLSStrategy**
- **Description:** Specific strategy attributes for MPLS.
- **Label:** MPLS Strategy
- **Icon:** eos-icons:neural-network
- **Menu Placement:** TopologyNetworkStrategy
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | choices |
| ---- | ---- | ------- |
| underlay | Dropdown | [{'name': 'ospf', 'label': 'OSPF'}, {'name': 'isis', 'label': 'ISIS'}, {'name': 'bgp', 'label': 'BGP'}] |
| overlay | Dropdown | [{'name': 'ldp', 'label': 'LDP'}, {'name': 'rsvp', 'label': 'RSVP'}, {'name': 'segment_routing', 'label': 'Segment Routing'}] |

### **EVPNStrategy**
- **Description:** Specific strategy attributes for EVPN.
- **Label:** EVPN Strategy
- **Icon:** carbon:load-balancer-network
- **Menu Placement:** TopologyNetworkStrategy
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | choices |
| ---- | ---- | ------- |
| underlay | Dropdown | [{'name': 'ebgp', 'label': 'EBGP'}, {'name': 'ospf', 'label': 'OSPF'}, {'name': 'isis', 'label': 'ISIS'}] |
| overlay | Dropdown | [{'name': 'ebgp', 'label': 'EBGP'}, {'name': 'ibgp', 'label': 'IBGP'}] |

### **PhysicalElement**
- **Description:** Physical aspect of topology elements.
- **Label:** Physical Topology Element
- **Icon:** carbon:network-3-reference
- **Menu Placement:** TopologyTopology
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | default_value | order_weight | label | choices |
| ---- | ---- | ------------- | ------------ | ----- | ------- |
| mtu | Number | 1500 | 3000 |  |  |
| border | Boolean | False | 2400 | Is a Topology Border |  |
| mlag_support | Boolean | False | 2500 | MLAG Support |  |
| device_role | Dropdown |  | 1300 | Role | [{'name': 'spine', 'color': '#ffb3ba'}, {'name': 'leaf', 'color': '#ffdfba'}, {'name': 'pe_router', 'color': '#baffc9'}, {'name': 'p_router', 'color': '#bae1ff'}, {'name': 'route_reflector', 'color': '#ffbaba'}, {'name': 'cpe', 'color': '#f2bae1'}, {'name': 'firewall', 'color': '#c5a3ff'}] |

#### Relationships
| name | label | peer | optional | cardinality | kind | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ---- | ------------ |
| device_type | Type | DcimDeviceType | True | one | Attribute | 1400 |

### **DhcpOption**
- **Description:** Represents a configurable option within a Dhcp server.
- **Label:** Dhcp Option
- **Icon:** gis:globe-options
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| name | Text | 1000 |  |
| description | Text | 1100 | True |
| option_code | Number | 2000 |  |
| content | Text | 2100 |  |

### **DhcpServer**
- **Description:** Represents a Dhcp server in the network.
- **Label:** Dhcp Server
- **Icon:** eos-icons:ip
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | order_weight |
| ---- | ---- | ------------ |
| lease_time | Text | 2100 |

#### Relationships
| name | peer | optional | cardinality | kind |
| ---- | ---- | -------- | ----------- | ---- |
| dhcp_options | NetworkDhcpOption | True | many | Component |

### **NameServer**
- **Description:** Represents a DNS server in the network.
- **Label:** DNS Server
- **Icon:** eos-icons:dns
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
### **NTPServer**
- **Description:** Represents a NTP server in the network.
- **Label:** NTP Server
- **Icon:** iconoir:time-zone
- **Menu Placement:** NetworkManagementServer
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
### **NetworkServiceIdentifier**
- **Description:** Generic model for different types of identifiers used in network services.
- **Label:** Network Service Identifier
- **Icon:** mdi:identifier
- **Menu Placement:** TopologyNetworkService
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** identifier__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind |
| ---- | ---- |
| identifier | Number |

#### Relationships
| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| service | Network Service | TopologyNetworkService | one | True |

### **NetworkService**
- **Description:** Network services attached to a Topology.
- **Label:** Network Service
- **Icon:** carbon:ibm-cloud-internet-services
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | label | kind | order_weight | enum |
| ---- | ----- | ---- | ------------ | ---- |
| name | Service Name | Text | 1000 |  |
| description |  | Text | 1100 |  |
| service_type |  | Text | 1200 | ['Layer2', 'Layer3'] |

#### Relationships
| name | peer | cardinality | kind | optional | order_weight |
| ---- | ---- | ----------- | ---- | -------- | ------------ |
| identifier | TopologyNetworkServiceIdentifier | one | Attribute | False |  |
| topology | TopologyTopology | one | Parent | False |  |
| vlan | InfraVLAN | one | Component | True | 1500 |
| prefix | InfraPrefix | one | Component | True | 1400 |

## Extensions
### DcimGenericDevice
#### Attributes
|  |
|  |

#### Relationships
| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| topology | TopologyTopology | True | one |

### IpamPrefix
#### Attributes
|  |
|  |

#### Relationships
| name | label | peer | optional | cardinality | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ------------ |
| network_service | Network Service | TopologyNetworkService | True | one | 1400 |
