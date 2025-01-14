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
| name | Text | 1000 |  | `` |
| description | Text | 2000 | True | `` |
| connector_type | Dropdown | 1100 |  | `FC, LC, LC_PC, LC_UPC, LC_APC, LSH, LSH_PC, LSH_UPC, LSH_APC, LX_5, LX_5_PC, LX_5_UPC, LX_5_APC, MPO, MTRJ, SC, SC_PC, SC_UPC, SC_APC, ST, CS, SN, SMA_905, SMA_906, URM_P2` |

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
| name | Text | 1000 |  |  |  | `` |
| position | Number | 1100 | Position for the module inside the Patch Panel. |  |  | `` |
| module_type | Dropdown | 1200 | Type of module inserted into the patch panel. | Module Type | True | `3_mpo_24_fo_lc` |
| serial | Text | 1500 |  |  | True | `` |
| description | Text | 2000 |  |  | True | `` |

#### Relationships
| name | peer | optional | order_weight | cardinality | kind |
| ---- | ---- | -------- | ------------ | ----------- | ---- |
| patch_panel | DcimPatchPanel | False | 900 | one | Parent |
