# SFP

This schema extension gives you all the models you need to document Small Form-factor Pluggable (SFP).

You can either plug it into an interface or attach it to a location (e.g. it's a spare SFP stored in a rack).

Improvements:

- As of now there is no verification with type / form factor / protocol / distance ...
- You could plug any SFP into any equipment interface (e.g. a virtual interface ...)
- You could link a SFP to an interface AND a location ...


Dependencies: `base`

## Overview

- **Version:** 1.0

## Generics

### GenericSFP

- **Description:** Generic base for all Small Form-factor Pluggable (SFP) transceivers.
- **Label:** SFP
- **Icon:** mdi:gpu
- **Include in Menu:** ✅

#### Attributes

| name | kind | optional | order_weight | description | choices | default_value |
| ---- | ---- | -------- | ------------ | ----------- | ------- | ------------- |
| serial | Text | True | 1400 |  | `` |  |
| sfp_type | Dropdown | False | 1100 | Type of SFP, such as LR, SR, T. | `lr, sr, lrm, t, sr4, lr4, zr, er, dac, aoc` |  |
| status | Dropdown | False | 1300 |  | `plugged, spare, decommissioned` | plugged |
| form_factor | Dropdown | False | 1000 | The physical form factor of the SFP module. | `sfp, sfp_plus, qsfp, qsfp_plus, qsfp28, qsfp_dd, cfp, cfp2, cfp4, xfp, sfp56, qsfp56, osfp` |  |

#### Relationships

| name | peer | kind | optional | cardinality | order_weight |
| ---- | ---- | ---- | -------- | ----------- | ------------ |
| interface | DcimInterface | Attribute | True | one | 1200 |
| spare_location | LocationHosting | Attribute | True | one | 1500 |
| manufacturer | OrganizationManufacturer | Attribute | True | one | 1350 |

## Nodes

### StandardSFP

- **Description:** Standard SFP module for various types (e.g., LR, SR, T).
- **Label:** Standard SFP
- **Icon:** mdi:gpu
- **Menu Placement:** DcimGenericSFP
- **Include in Menu:** ❌

### BidiSFP

- **Description:** Bidirectional SFP supporting two wavelengths for single-fiber operation.
- **Label:** Bidirectional SFP
- **Icon:** lineicons:arrow-both-direction-vertical-1
- **Menu Placement:** DcimGenericSFP
- **Include in Menu:** ❌

#### Attributes

| name | label | kind | optional | description | order_weight |
| ---- | ----- | ---- | -------- | ----------- | ------------ |
| wavelength_tx | Transmit Wavelength (nm) | Number | False | Transmit wavelength in nm. | 1175 |
| wavelength_rx | Receive Wavelength (nm) | Number | False | Receive wavelength in nm. | 1150 |

## Extensions
### DcimInterface
#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| plugged_sfp | DcimGenericSFP | one | True |

### LocationHosting
#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| spare_sfps | DcimGenericSFP | many | True |

### OrganizationManufacturer
#### Relationships

| name | label | peer | cardinality | optional |
| ---- | ----- | ---- | ----------- | -------- |
| sfps | SFPs | DcimGenericSFP | many | True |
