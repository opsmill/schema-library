# DWDM

This schema extension contains models for OADM (Optical Add Drop Multiplexer) supporting various WDM (Wavelength Division Multiplexing) technologies such as DWDM (Dense Wavelength Division Multiplexing) or CWDM (Coarse Wavelength Division Multiplexing). With some vendors, the tunable optics are not configured via the channel number but via the wavelength and/or the frequency. This model provides a unique entry in Infrahub for those.


Dependencies: `base, extensions.sfp`
## Overview
- **Version:** 1.0
## Generics
### **GenericOadmInterface**
- **Label:** Optical Multiplexer Interfaces
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimOpticalMultiplexer
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | order_weight | optional | choices |
| ---- | ---- | ------------ | -------- | ------- |
| name | Text | 1000 |  |  |
| description | Text | 2000 | True |  |
| connector_type | Dropdown | 1100 |  | [{'name': 'FC', 'label': 'FC', 'description': 'Standardized fiber optic connector used primarily in datacom and telecom applications.'}, {'name': 'LC', 'label': 'LC', 'description': 'Compact fiber optic connector with a push-pull mechanism.'}, {'name': 'LC_PC', 'label': 'LC/PC', 'description': 'Polished LC connector providing physical contact (PC).'}, {'name': 'LC_UPC', 'label': 'LC/UPC', 'description': 'Ultra-Physical Contact (UPC) variant of the LC connector with enhanced polish.'}, {'name': 'LC_APC', 'label': 'LC/APC', 'description': 'Angled Physical Contact (APC) version of the LC connector with a slanted fiber end-face.'}, {'name': 'LSH', 'label': 'LSH', 'description': 'European fiber optic connector offering high durability.'}, {'name': 'LSH_PC', 'label': 'LSH/PC', 'description': 'Physical Contact version of LSH with standard polish.'}, {'name': 'LSH_UPC', 'label': 'LSH/UPC', 'description': 'Ultra-Physical Contact variant of LSH, minimizing return loss with a superior polish.'}, {'name': 'LSH_APC', 'label': 'LSH/APC', 'description': 'Angled Physical Contact version of LSH, designed to reduce back reflections.'}, {'name': 'LX_5', 'label': 'LX.5', 'description': 'Miniaturized fiber optic connector similar to LC but with an additional shutter mechanism.'}, {'name': 'LX_5_PC', 'label': 'LX.5/PC', 'description': 'Physical Contact version of LX.5.'}, {'name': 'LX_5_UPC', 'label': 'LX.5/UPC', 'description': 'Ultra-Physical Contact variant of LX.5.'}, {'name': 'LX_5_APC', 'label': 'LX.5/APC', 'description': 'Angled Physical Contact version of LX.5.'}, {'name': 'MPO', 'label': 'MPO', 'description': 'Multi-fiber Push-On connector typically used in data centers for high-speed applications.'}, {'name': 'MTRJ', 'label': 'MTRJ', 'description': 'Male-to-female fiber optic connector with two fibers.'}, {'name': 'SC', 'label': 'SC', 'description': 'Square fiber optic connector with push-pull lock.'}, {'name': 'SC_PC', 'label': 'SC/PC', 'description': 'Physical Contact SC connector with a polished end-face.'}, {'name': 'SC_UPC', 'label': 'SC/UPC', 'description': 'Ultra-Physical Contact variant of SC.'}, {'name': 'SC_APC', 'label': 'SC/APC', 'description': 'Angled Physical Contact version of SC.'}, {'name': 'ST', 'label': 'ST', 'description': 'Bayonet-style fiber optic connector primarily used in industrial and military applications.'}, {'name': 'CS', 'label': 'CS', 'description': 'Compact connector with a high-density duplex configuration.'}, {'name': 'SN', 'label': 'SN', 'description': 'Small-form connector with dual fibers.'}, {'name': 'SMA_905', 'label': 'SMA 905', 'description': 'Stainless steel fiber optic connector.'}, {'name': 'SMA_906', 'label': 'SMA 906', 'description': 'Variant of SMA 905 with similar durability, frequently used in high-vibration settings.'}, {'name': 'URM_P2', 'label': 'URM-P2', 'description': 'Specialized fiber optic connector for industrial and harsh environments.'}] |

## Nodes
### **OpticalMultiplexer**
- **Description:** An OADM (Optical Add Drop Multiplexer) supporting various WDM (Wavelength Division Multiplexing) technologies.
- **Label:** Optical Multiplexer
- **Icon:** mdi:transit-connection-variant
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | order_weight | description | optional | choices | default_value |
| ---- | ---- | ------------ | ----------- | -------- | ------- | ------------- |
| name | Text | 1000 |  |  |  |  |
| wdm_type | Dropdown | 1110 | Type of WDM (e.g CWDM. DWDM) | False | [{'name': 'cwdm', 'label': 'CWDM (Coarse Wavelength Division Multiplexing)', 'description': 'Supports multiple wavelengths for communication up to 70km.', 'color': '#0099cc'}, {'name': 'dwdm', 'label': 'DWDM (Dense Wavelength Division Multiplexing)', 'description': 'Supports dense wavelengths and amplification for long-distance communication.', 'color': '#9933cc'}] | dwdm |
| description | Text | 2000 |  | True |  |  |

#### Relationships
| name | peer | identifier | optional | cardinality | kind |
| ---- | ---- | ---------- | -------- | ----------- | ---- |
| front_interfaces | DcimOadmFrontInterface | front_interfaces | True | many | Component |
| rear_interface | DcimOadmRearInterface | rear_interfaces | True | one | Component |

### **OadmFrontInterface**
- **Label:** Optical Multiplexer Front Interfaces
- **Menu Placement:** DcimGenericOadmInterface
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** optical_multiplexer__name__value, name__value
- **Uniqueness Constraints:** optical_multiplexer + name__value
---
#### Relationships
| name | peer | order_weight | identifier | optional | cardinality | kind |
| ---- | ---- | ------------ | ---------- | -------- | ----------- | ---- |
| optical_multiplexer | DcimOpticalMultiplexer | 900 | front_interfaces | False | one | Parent |
| channels | DcimWdmChannel | 1200 |  | True | many | Attribute |

### **OadmRearInterface**
- **Label:** Optical Multiplexer Rear Interfaces
- **Menu Placement:** DcimGenericOadmInterface
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** optical_multiplexer__name__value, name__value
- **Uniqueness Constraints:** optical_multiplexer + name__value
---
#### Relationships
| name | peer | order_weight | identifier | optional | cardinality | kind |
| ---- | ---- | ------------ | ---------- | -------- | ----------- | ---- |
| optical_multiplexer | DcimOpticalMultiplexer | 900 | rear_interface | False | one | Parent |

### **WdmChannel**
- **Description:** A WDM channel with its wavelength and frequency.
- **Label:** WDM Channel
- **Icon:** game-icons:laser-warning
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** wdm_type__value, channel__value
- **Uniqueness Constraints:** wdm_type__value + channel__value + wavelength__value + frequency__value, wdm_type__value + channel__value
---
#### Attributes
| name | kind | description | order_weight | optional | choices | default_value | label |
| ---- | ---- | ----------- | ------------ | -------- | ------- | ------------- | ----- |
| channel | Number | WDM channel number. |  |  |  |  |  |
| wdm_type | Dropdown | Type of WDM (e.g CWDM. DWDM) | 1110 | False | [{'name': 'cwdm', 'label': 'CWDM (Coarse Wavelength Division Multiplexing)', 'description': 'Supports multiple wavelengths for communication up to 70km.', 'color': '#0099cc'}, {'name': 'dwdm', 'label': 'DWDM (Dense Wavelength Division Multiplexing)', 'description': 'Supports dense wavelengths and amplification for long-distance communication.', 'color': '#9933cc'}] | dwdm |  |
| wavelength | Text | Wavelength of the channel in nm. |  |  |  |  | Wavelength (nm) |
| frequency | Text | Frequency of the channel in GHz. |  |  |  |  | Frequency (GHz) |

### **WdmSFP**
- **Description:** SFP with configuration for Wavelength Division Multiplexing.
- **Label:** WDM SFP
- **Icon:** mdi:laser-pointer
- **Menu Placement:** DcimGenericSFP
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | description | order_weight | optional | choices | default_value |
| ---- | ---- | ----------- | ------------ | -------- | ------- | ------------- |
| wdm_type | Dropdown | Type of WDM (e.g CWDM. DWDM) | 1110 | False | [{'name': 'cwdm', 'label': 'CWDM (Coarse Wavelength Division Multiplexing)', 'description': 'Supports multiple wavelengths for communication up to 70km.', 'color': '#0099cc'}, {'name': 'dwdm', 'label': 'DWDM (Dense Wavelength Division Multiplexing)', 'description': 'Supports dense wavelengths and amplification for long-distance communication.', 'color': '#9933cc'}] | dwdm |

#### Relationships
| name | label | peer | kind | cardinality | optional | order_weight |
| ---- | ----- | ---- | ---- | ----------- | -------- | ------------ |
| wdm_channel | WDM Channel | DcimWdmChannel | Attribute | one | False | 1150 |
