# Location Minimal

This schema extension is minimal but will provide you with basic items to store location related data.

Dependencies: `base`

## Overview

- **Version:** 1.0

## Nodes

### Country

- **Label:** Country
- **Icon:** gis:search-country
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ❌

#### Attributes

| name | kind | optional | order_weight |
| ---- | ---- | -------- | ------------ |
| timezone | Text | True | 1300 |

### Metro

- **Label:** Metro
- **Icon:** healthicons:city
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ❌

### Site

- **Label:** Site
- **Icon:** ri:building-line
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ❌

#### Attributes

| name | kind | unique | optional | order_weight |
| ---- | ---- | ------ | -------- | ------------ |
| facility\_id | Text | False | True | 1100 |
| physical\_address | Text | False | True | 1500 |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| owner | OrganizationGeneric | True | one |

### Rack

- **Label:** Rack
- **Icon:** clarity:rack-server-line
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

#### Attributes

| name | kind | unique | optional | order_weight | label | default_value |
| ---- | ---- | ------ | -------- | ------------ | ----- | ------------- |
| facility\_id | Text | False | True | 1100 |  |  |
| height | Number |  | False | 1300 | Height \(U\) | 42 |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| owner | OrganizationGeneric | True | one |

## Extensions

### OrganizationProvider

#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| sites | LocationSite | many | True |
