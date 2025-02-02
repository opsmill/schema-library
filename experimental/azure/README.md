# Azure

This schema extension introduces cloud support for Microsoft Azure.

Dependencies: `base`

Attribution: [Rowan Coleman](https://www.linkedin.com/in/rowan-coleman-6a147156/)

## azure

- **Version:** 1.0

## Generics

### Resource

- **Label:** Azure
- **Include in Menu:** ✅

#### Attributes

| name | kind |
| ---- | ---- |
| name | Text |

#### Relationships

| name | cardinality | kind | peer | optional |
| ---- | ----------- | ---- | ---- | -------- |
| location | one | Attribute | AzureLocation |  |
| resourcegroup | one | Parent | AzureResourceGroup | False |

## Nodes

### Location

- **Menu Placement:** AzureResource
- **Include in Menu:** ❌

#### Attributes

| name | kind |
| ---- | ---- |
| name | Text |

### Tenant

- **Menu Placement:** AzureResource
- **Include in Menu:** ❌

#### Attributes

| name | kind |
| ---- | ---- |
| name | Text |
| tenant\_id | Text |

#### Relationships

| name | cardinality | peer | kind |
| ---- | ----------- | ---- | ---- |
| subscriptions | many | AzureSubscription | Component |

### Subscription

- **Menu Placement:** AzureResource
- **Include in Menu:** ❌

#### Attributes

| name | kind |
| ---- | ---- |
| name | Text |
| subscription\_id | Text |

#### Relationships

| name | cardinality | peer | kind | optional |
| ---- | ----------- | ---- | ---- | -------- |
| tenant | one | AzureTenant | Parent | False |
| resourcegroups | many | AzureResourceGroup | Component |  |

### ResourceGroup

- **Menu Placement:** AzureResource
- **Include in Menu:** ❌

#### Attributes

| name | kind |
| ---- | ---- |
| name | Text |

#### Relationships

| name | cardinality | kind | peer | optional |
| ---- | ----------- | ---- | ---- | -------- |
| location | one | Attribute | AzureLocation |  |
| subscription | one | Parent | AzureSubscription | False |

### VirtualNetwork

- **Label:** Virtual Networks
- **Menu Placement:** AzureResource
- **Include in Menu:** ❌

#### Relationships

| name | cardinality | kind | peer |
| ---- | ----------- | ---- | ---- |
| address\_space | many | Attribute | BuiltinIPPrefix |
| subnets | many | Component | AzureVirtualNetworkSubnet |

### VirtualNetworkSubnet

- **Label:** Subnets
- **Menu Placement:** AzureResource
- **Include in Menu:** ✅

#### Attributes

| name | kind |
| ---- | ---- |
| name | Text |

#### Relationships

| name | cardinality | peer | kind | optional |
| ---- | ----------- | ---- | ---- | -------- |
| virtualnetwork | one | AzureVirtualNetwork | Parent | False |
| address\_prefixes | many | BuiltinIPPrefix | Attribute |  |
