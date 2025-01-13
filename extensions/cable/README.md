# Cable

This schema extension contains a basic Cable model allowing you to connect two endpoints.


Dependencies: `base`
## Overview
- **Version:** 1.0
## Nodes
### **Cable**
- **Description:** Physical cable connecting two endpoints
- **Label:** Cable
- **Icon:** mdi:cable-data
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | optional | order_weight | choices | label |
| ---- | ---- | -------- | ------------ | ------- | ----- |
| status | Dropdown | True | 1000 | `connected, planned` |  |
| cable_type | Dropdown | True | 1100 | `cat3, cat5, cat5e, cat6, cat6a, cat7, cat7a, cat8, mmf-om1, mmf-om2, mmf-om3, mmf-om4, mmf-om5, smf-os1, smf-os2, dac-passive, dac-active, aoc, coaxial, mrj21-trunk, power, usb` |  |
| color | Dropdown | True | 1300 | `dark-red, red, pink, rose, fuchsia, purple, dark-purple, indigo, blue, light-blue, cyan, teal, aqua, dark-green, green, light-green, lime, yellow, amber, orange, dark-orange, brown, light-grey, grey, dark-grey, black` |  |
| label | Text | True | 1200 | `` |  |
| length | Number | True | 1350 | `` | Length (in cm) |
