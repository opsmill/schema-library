## Location Extended

This schema extension is the most detailed when it comes to location, you'll find all the layers you can think of.

- **Dependencies:** `base`
- **Version:** 1.0

### Nodes

#### Continent

- **Label:** Continent
- **Icon:** jam:world
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

#### Country

- **Label:** Country
- **Icon:** gis:search-country
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

#### Region

- **Label:** Region
- **Icon:** carbon:cics-region-target
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

#### Metro

- **Label:** Metro
- **Icon:** healthicons:city
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

#### Building

- **Label:** Building
- **Icon:** ri:building-line
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

##### Attributes

| name | kind | unique | optional | order_weight |
| ---- | ---- | ------ | -------- | ------------ |
| facility\_id | Text | False | True | 1100 |
| physical\_address | Text | False | True | 1500 |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| owner | OrganizationGeneric | True | one |

#### Floor

- **Label:** Floor
- **Icon:** mdi:home-floor-0
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

#### Suite

- **Label:** Suite
- **Icon:** game-icons:cage
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

##### Attributes

| name | kind | unique | optional | order_weight |
| ---- | ---- | ------ | -------- | ------------ |
| facility\_id | Text | False | True | 1100 |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| owner | OrganizationGeneric | True | one |

#### Rack

- **Label:** Rack
- **Icon:** clarity:rack-server-line
- **Menu Placement:** LocationGeneric
- **Include in Menu:** ✅

##### Attributes

| name | kind | unique | optional | order_weight |
| ---- | ---- | ------ | -------- | ------------ |
| facility\_id | Text | False | True | 1100 |

#### Relationships

| name | peer | optional | cardinality |
| ---- | ---- | -------- | ----------- |
| owner | OrganizationGeneric | True | one |

### Extensions

#### OrganizationProvider

#### Relationships

| name | peer | cardinality | optional |
| ---- | ---- | ----------- | -------- |
| location | LocationBuilding | many | True |
