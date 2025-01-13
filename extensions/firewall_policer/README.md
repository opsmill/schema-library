# Firewall Policer

This schema extension contains models for VMs. You might consider Cluster or/and Hypervisor extension to go with!


## Overview
- **Version:** 1.0
## Nodes
### **Policer**
- **Description:** A generic policer configuration.
- **Label:** Network Policer
- **Icon:** mdi:car-speed-limiter
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value
---
#### Attributes
| name | kind | label | description | order_weight | unique | optional | choices |
| ---- | ---- | ----- | ----------- | ------------ | ------ | -------- | ------- |
| name | Text | Name | Unique name of the policer. | 1000 | True |  |  |
| description | Text |  |  | 1100 |  | True |  |
| policer_type | Dropdown | Policer Type | Type of policer. | 1150 |  | True | [{'name': 'bandwidth-policer', 'label': 'Bandwidth Policer', 'description': 'Policer that limits bandwidth on interfaces.', 'color': '#C3E0E5'}, {'name': 'interface-policer', 'label': 'Interface Policer', 'description': 'Policer applied to interfaces for rate-limiting traffic.', 'color': '#D1E7E1'}, {'name': 'shared-policer', 'label': 'Shared Policer', 'description': 'Policer with shared bandwidth across multiple links.', 'color': '#A5C9C7'}, {'name': 'hierarchical-policer', 'label': 'Hierarchical Policer', 'description': 'Policer applied in a hierarchical manner (e.g., parent-child relationships).', 'color': '#B1E0D9'}] |
| bandwidth_limit | Dropdown | Bandwidth Limit | Bandwidth limit for the policer. | 1200 |  | True | [{'name': '500k', 'label': '500 Kbps', 'description': 'Bandwidth limit of 500 Kbps.', 'color': '#A9CCE3'}, {'name': '2125k', 'label': '2,125 Kbps', 'description': 'Bandwidth limit of 2,125 Kbps.', 'color': '#AED6F1'}, {'name': '5250k', 'label': '5,250 Kbps', 'description': 'Bandwidth limit of 5,250 Kbps.', 'color': '#B4DDED'}, {'name': '10m', 'label': '10 Mbps', 'description': 'Bandwidth limit of 10 Mbps.', 'color': '#C2E2F3'}, {'name': '20m', 'label': '20 Mbps', 'description': 'Bandwidth limit of 20 Mbps.', 'color': '#D0E7F8'}, {'name': '30m', 'label': '30 Mbps', 'description': 'Bandwidth limit of 30 Mbps.', 'color': '#E0ECF9'}, {'name': '50m', 'label': '50 Mbps', 'description': 'Bandwidth limit of 50 Mbps.', 'color': '#AFC7F2'}, {'name': '75m', 'label': '75 Mbps', 'description': 'Bandwidth limit of 75 Mbps.', 'color': '#E8F3FD'}, {'name': '100m', 'label': '100 Mbps', 'description': 'Bandwidth limit of 100 Mbps.', 'color': '#F0F9FF'}, {'name': '200m', 'label': '200 Mbps', 'description': 'Bandwidth limit of 200 Mbps.', 'color': '#D1E6F9'}, {'name': '300m', 'label': '300 Mbps', 'description': 'Bandwidth limit of 300 Mbps.', 'color': '#EAF2FC'}, {'name': '1000m', 'label': '1 Gbps', 'description': 'Bandwidth limit of 1 Gbps.', 'color': '#E6E6FA'}] |
| pps_limit | Dropdown | PPS Limit | Packets per second (PPS) limit for the policer. | 1250 |  | True | [{'name': '500pps', 'label': '500 PPS', 'description': 'PPS limit of 500.', 'color': '#E0BBE4'}, {'name': '1000pps', 'label': '1,000 PPS', 'description': 'PPS limit of 1,000.', 'color': '#D4A5E4'}, {'name': '5000pps', 'label': '5,000 PPS', 'description': 'PPS limit of 5,000.', 'color': '#C89BE4'}] |
| burst_size_limit | Dropdown | Burst Size Limit | Burst size limit for the policer. | 1300 |  | True | [{'name': '50k', 'label': '50 KB', 'description': 'Burst size limit of 50 KB.', 'color': '#CDEACC'}, {'name': '100k', 'label': '100 KB', 'description': 'Burst size limit of 100 KB.', 'color': '#B3E2A8'}, {'name': '128k', 'label': '128 KB', 'description': 'Burst size limit of 128 KB.', 'color': '#A3D89E'}, {'name': '256k', 'label': '256 KB', 'description': 'Burst size limit of 256 KB.', 'color': '#92CF91'}, {'name': '512k', 'label': '512 KB', 'description': 'Burst size limit of 512 KB.', 'color': '#88C786'}, {'name': '1m', 'label': '1 MB', 'description': 'Burst size limit of 1 MB.', 'color': '#7FCF79'}, {'name': '1500k', 'label': '1.5 MB', 'description': 'Burst size limit of 1.5 MB.', 'color': '#77C46B'}, {'name': '2m', 'label': '2 MB', 'description': 'Burst size limit of 2 MB.', 'color': '#63A17E'}, {'name': '3m', 'label': '3 MB', 'description': 'Burst size limit of 3 MB.', 'color': '#8FD19E'}, {'name': '4m', 'label': '4 MB', 'description': 'Burst size limit of 4 MB.', 'color': '#70B961'}, {'name': '8m', 'label': '8 MB', 'description': 'Burst size limit of 8 MB.', 'color': '#6BAD57'}, {'name': '12m', 'label': '12 MB', 'description': 'Burst size limit of 12 MB.', 'color': '#63A14C'}, {'name': '37m', 'label': '37 MB', 'description': 'Burst size limit of 37 MB.', 'color': '#56A56C'}, {'name': '40m', 'label': '40 MB', 'description': 'Burst size limit of 40 MB.', 'color': '#5F9742'}, {'name': '1000000k', 'label': '1 GB', 'description': 'Burst size limit of 1 GB.', 'color': '#599D4A'}] |
| packet_burst | Dropdown | Packet Burst | Packet burst size for the policer. | 1350 |  | True | [{'name': '1k', 'label': '1,000 packets', 'description': 'Packet burst size of 1,000 packets.', 'color': '#FFE4E1'}, {'name': '5k', 'label': '5,000 packets', 'description': 'Packet burst size of 5,000 packets.', 'color': '#FFFACD'}, {'name': '10k', 'label': '10,000 packets', 'description': 'Packet burst size of 10,000 packets.', 'color': '#FFF0F5'}] |
| action | Dropdown | Action | Action to take when limits are exceeded. | 1400 |  |  | [{'name': 'discard', 'label': 'Discard', 'description': 'Discard the packet.', 'color': '#F4CCCC'}, {'name': 'drop', 'label': 'Drop', 'description': 'Drop the packet.', 'color': '#FAD7A0'}, {'name': 'accept', 'label': 'Accept', 'description': 'Accept the packet.', 'color': '#CDEACC'}] |
