# Tenancy

This schema extension introduces tenancy for some of the schema nodes (circuits...)

Dependencies: `base, extensions.circuit, experimental.location_extended`

## tenancy

- **Version:** 1.0

## Nodes

### Tenant

- **Description:** A tenant is owning the corresponding entity
- **Icon:** mdi:domain
- **Include in Menu:** ✅

#### Relationships

| name | peer | cardinality | kind | optional | order_weight |
| ---- | ---- | ----------- | ---- | -------- | ------------ |
| tags | BuiltinTag | many | Attribute | True | 3000 |
| location | LocationBuilding | many |  | True |  |
| circuit | DcimCircuit | many |  | True |  |
