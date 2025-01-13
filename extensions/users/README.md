# Accounts Management

This schema extension contains models for Accounts management.


Dependencies: `base`
## Overview
- **Version:** 1.0
## Nodes
### **Group**
- **Description:** User Group
- **Label:** User Groups
- **Icon:** iconoir:group
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value
---
#### Attributes
| name | kind | order_weight | optional | label | choices |
| ---- | ---- | ------------ | -------- | ----- | ------- |
| name | Text | 1000 |  |  |  |
| description | Text | 1100 | True |  |  |
| idle_timeout | Number | 1300 |  | Idle Timeout (s) |  |
| permissions | Dropdown | 1200 | False |  | [{'name': 'admin', 'description': 'All rights on device.', 'color': '#E6E6FA'}, {'name': 'operator', 'description': 'Operator right on configuration.', 'color': '#E6E6FA'}, {'name': 'read-only', 'description': 'Read only right on configuration.', 'color': '#E6E6FA'}] |

### **Account**
- **Description:** User login and authentication
- **Label:** User Account
- **Icon:** mdi:account-key
- **Include in Menu:** ❌

#### Ordering and Constraints
- **Order By:** name__value
- **Uniqueness Constraints:** name__value
---
#### Attributes
| name | label | kind | optional | description | order_weight | default_value |
| ---- | ----- | ---- | -------- | ----------- | ------------ | ------------- |
| name | Username | Text | False | The login username | 1000 |  |
| full_name |  | Text | True | Full name of the account | 1100 |  |
| ssh_key |  | Password | True | SSH key for secure access | 1300 |  |
| password |  | Password | True | Password for login (alternative to SSH key) | 1400 |  |
| mfa_enabled |  | Boolean |  | Whether multi-factor authentication is enabled | 1500 | False |

#### Relationships
| name | peer | cardinality | optional | kind | order_weight |
| ---- | ---- | ----------- | -------- | ---- | ------------ |
| user_group | UserGroup | one | False | Attribute | 1200 |
| organization | OrganizationGeneric | one | False | Parent |  |

## Extensions
### OrganizationGeneric
#### Relationships
| name | kind | peer | description | cardinality |
| ---- | ---- | ---- | ----------- | ----------- |
| accounts | Component | UserAccount | List of Accounts under this organization | many |
