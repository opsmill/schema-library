# Firewall Policer

This schema extension contains models for VMs. You might consider Cluster or/and Hypervisor extension to go with!

## Overview

- **Version:** 1.0

## Nodes

### Policer

- **Description:** A generic policer configuration.
- **Label:** Network Policer
- **Icon:** mdi:car-speed-limiter
- **Include in Menu:** ❌


#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value
#### Attributes

| name | kind | label | description | order_weight | unique | optional | choices |
| ---- | ---- | ----- | ----------- | ------------ | ------ | -------- | ------- |
| name | Text | Name | Unique name of the policer. | 1000 | True |  | `` |
| description | Text |  |  | 1100 |  | True | `` |
| policer_type | Dropdown | Policer Type | Type of policer. | 1150 |  | True | `bandwidth-policer, interface-policer, shared-policer, hierarchical-policer` |
| bandwidth_limit | Dropdown | Bandwidth Limit | Bandwidth limit for the policer. | 1200 |  | True | `500k, 2125k, 5250k, 10m, 20m, 30m, 50m, 75m, 100m, 200m, 300m, 1000m` |
| pps_limit | Dropdown | PPS Limit | Packets per second (PPS) limit for the policer. | 1250 |  | True | `500pps, 1000pps, 5000pps` |
| burst_size_limit | Dropdown | Burst Size Limit | Burst size limit for the policer. | 1300 |  | True | `50k, 100k, 128k, 256k, 512k, 1m, 1500k, 2m, 3m, 4m, 8m, 12m, 37m, 40m, 1000000k` |
| packet_burst | Dropdown | Packet Burst | Packet burst size for the policer. | 1350 |  | True | `1k, 5k, 10k` |
| action | Dropdown | Action | Action to take when limits are exceeded. | 1400 |  |  | `discard, drop, accept` |
