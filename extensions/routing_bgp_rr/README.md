# BGP Route Reflector

This schema extension extend the BGP extension to add BGP Route Reflector Clustering.

Dependencies: `base, extensions.routing, extensions.routing_bgp`

## Overview

- **Version:** 1.0

## Nodes

### BGPRRCluster

- **Description:** A Route Reflector (RR) Cluster used for grouping internal peers
- **Label:** Route Reflector Cluster
- **Icon:** mdi:router-network
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**
- **Uniqueness Constraints:**name__value

#### Attributes

| name | kind | description | order_weight | optional |
| ---- | ---- | ----------- | ------------ | -------- |
| name | Text | Name of the Route Reflector Cluster | 1000 |  |
| description | Text | Optional description of the Route Reflector Cluster | 1100 | True |

#### Relationships

| name | label | peer | description | cardinality | kind | optional | order_weight |
| ---- | ----- | ---- | ----------- | ----------- | ---- | -------- | ------------ |
| cluster\_id | Cluster ID | IpamIPAddress | Cluster ID represented as a reference to an IP Address | one | Attribute | False | 1200 |
| peer\_groups | BGP Peer Groups | RoutingBGPPeerGroup |  | many | Generic | True |  |

## Extensions

### RoutingBGPPeerGroup

#### Relationships

| name | label | peer | cardinality | kind | order_weight |
| ---- | ----- | ---- | ----------- | ---- | ------------ |
| rr\_cluster | RR Cluster | RoutingBGPRRCluster | one | Attribute | 1600 |
