# Patch Panel

This schema extension allows you to capture patch pannel related information like rear/front interfaces and mapping between them. You can insert the patch panel into a rack and leverage the device type model. Finally you can also capture informations about potential modules you would insert into your patch panel.

> [!NOTE]
> This extension is compatible with all sort of connectors, meaning you can plug cable, circuits, cross-connect to front & rear interfaces!



## Overview
- **Version:** 1.0
## Generics
### **GenericPatchPanelInterface**
- **Label:** Patch Panel Interfaces
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimPatchPanel
- **Include in Menu:** ❌
---
#### Attributes
| name | kind | order_weight | optional | choices |
| ---- | ---- | ------------ | -------- | ------- |
| name | Text | 1000 |  |  |
| description | Text | 2000 | True |  |
| connector_type | Dropdown | 1100 |  | [{'name': 'FC', 'label': 'FC', 'description': 'Standardized fiber optic connector used primarily in datacom and telecom applications.'}, {'name': 'LC', 'label': 'LC', 'description': 'Compact fiber optic connector with a push-pull mechanism.'}, {'name': 'LC_PC', 'label': 'LC/PC', 'description': 'Polished LC connector providing physical contact (PC).'}, {'name': 'LC_UPC', 'label': 'LC/UPC', 'description': 'Ultra-Physical Contact (UPC) variant of the LC connector with enhanced polish.'}, {'name': 'LC_APC', 'label': 'LC/APC', 'description': 'Angled Physical Contact (APC) version of the LC connector with a slanted fiber end-face.'}, {'name': 'LSH', 'label': 'LSH', 'description': 'European fiber optic connector offering high durability.'}, {'name': 'LSH_PC', 'label': 'LSH/PC', 'description': 'Physical Contact version of LSH with standard polish.'}, {'name': 'LSH_UPC', 'label': 'LSH/UPC', 'description': 'Ultra-Physical Contact variant of LSH, minimizing return loss with a superior polish.'}, {'name': 'LSH_APC', 'label': 'LSH/APC', 'description': 'Angled Physical Contact version of LSH, designed to reduce back reflections.'}, {'name': 'LX_5', 'label': 'LX.5', 'description': 'Miniaturized fiber optic connector similar to LC but with an additional shutter mechanism.'}, {'name': 'LX_5_PC', 'label': 'LX.5/PC', 'description': 'Physical Contact version of LX.5.'}, {'name': 'LX_5_UPC', 'label': 'LX.5/UPC', 'description': 'Ultra-Physical Contact variant of LX.5.'}, {'name': 'LX_5_APC', 'label': 'LX.5/APC', 'description': 'Angled Physical Contact version of LX.5.'}, {'name': 'MPO', 'label': 'MPO', 'description': 'Multi-fiber Push-On connector typically used in data centers for high-speed applications.'}, {'name': 'MTRJ', 'label': 'MTRJ', 'description': 'Male-to-female fiber optic connector with two fibers.'}, {'name': 'SC', 'label': 'SC', 'description': 'Square fiber optic connector with push-pull lock.'}, {'name': 'SC_PC', 'label': 'SC/PC', 'description': 'Physical Contact SC connector with a polished end-face.'}, {'name': 'SC_UPC', 'label': 'SC/UPC', 'description': 'Ultra-Physical Contact variant of SC.'}, {'name': 'SC_APC', 'label': 'SC/APC', 'description': 'Angled Physical Contact version of SC.'}, {'name': 'ST', 'label': 'ST', 'description': 'Bayonet-style fiber optic connector primarily used in industrial and military applications.'}, {'name': 'CS', 'label': 'CS', 'description': 'Compact connector with a high-density duplex configuration.'}, {'name': 'SN', 'label': 'SN', 'description': 'Small-form connector with dual fibers.'}, {'name': 'SMA_905', 'label': 'SMA 905', 'description': 'Stainless steel fiber optic connector.'}, {'name': 'SMA_906', 'label': 'SMA 906', 'description': 'Variant of SMA 905 with similar durability, frequently used in high-vibration settings.'}, {'name': 'URM_P2', 'label': 'URM-P2', 'description': 'Specialized fiber optic connector for industrial and harsh environments.'}] |

## Nodes
### **PatchPanel**
- **Description:** A Patch Panel used for managing network cable connections in a data center or telecom setup.
- **Label:** Patch Panel
- **Icon:** ic:round-device-hub
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** 
---
#### Attributes
| name | kind | unique | order_weight | label | optional | description |
| ---- | ---- | ------ | ------------ | ----- | -------- | ----------- |
| name | Text | True | 1000 |  |  |  |
| module_capacity | Number |  |  | Module Capacity | True | The maximum number of modules that can be housed within this patch panel. |
| description | Text |  | 2000 |  | True |  |

#### Relationships
| name | peer | identifier | optional | cardinality | kind |
| ---- | ---- | ---------- | -------- | ----------- | ---- |
| front_interfaces | DcimFrontPatchPanelInterface | front_interfaces | True | many | Component |
| rear_interfaces | DcimRearPatchPanelInterface | rear_interfaces | True | many | Component |
| modules | DcimPatchPanelModule |  | True | many | Component |

### **FrontPatchPanelInterface**
- **Label:** Patch Panel Front Interfaces
- **Menu Placement:** DcimGenericPatchPanelInterface
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** corresponding_front_rear__name__value, name__value
- **Uniqueness Constraints:** patch_panel + name__value
---
#### Relationships
| name | label | peer | order_weight | optional | cardinality | kind | identifier |
| ---- | ----- | ---- | ------------ | -------- | ----------- | ---- | ---------- |
| corresponding_front_rear | Corresponding rear interface | DcimRearPatchPanelInterface | 1200 | True | one | Attribute |  |
| patch_panel |  | DcimPatchPanel | 900 | False | one | Parent | front_interfaces |

### **RearPatchPanelInterface**
- **Label:** Patch Panel Rear Interfaces
- **Menu Placement:** DcimGenericPatchPanelInterface
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** patch_panel__name__value, name__value
- **Uniqueness Constraints:** patch_panel + name__value
---
#### Relationships
| name | label | peer | order_weight | optional | cardinality | kind | identifier |
| ---- | ----- | ---- | ------------ | -------- | ----------- | ---- | ---------- |
| corresponding_front_rear | Corresponding front interfaces | DcimFrontPatchPanelInterface | 1200 | True | many | Attribute |  |
| patch_panel |  | DcimPatchPanel | 900 | False | one | Parent | rear_interfaces |

### **PatchPanelModule**
- **Label:** Patch Panel Module
- **Icon:** mdi:expansion-card
- **Menu Placement:** DcimPatchPanel
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** patch_panel__name__value, position__value
- **Uniqueness Constraints:** patch_panel + position__value
---
#### Attributes
| name | kind | order_weight | description | label | optional | choices |
| ---- | ---- | ------------ | ----------- | ----- | -------- | ------- |
| name | Text | 1000 |  |  |  |  |
| position | Number | 1100 | Position for the module inside the Patch Panel. |  |  |  |
| module_type | Dropdown | 1200 | Type of module inserted into the patch panel. | Module Type | True | [{'name': '3_mpo_24_fo_lc', 'label': '24 FO LC 3 MPO', 'description': 'High-density MPO cassette with 24 fibers to front and 3 MPO to rear.', 'color': '#7f7fff'}] |
| serial | Text | 1500 |  |  | True |  |
| description | Text | 2000 |  |  | True |  |

#### Relationships
| name | peer | optional | order_weight | cardinality | kind |
| ---- | ---- | -------- | ------------ | ----------- | ---- |
| patch_panel | DcimPatchPanel | False | 900 | one | Parent |
