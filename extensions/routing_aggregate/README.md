# Aggregate

This schema extension contains all you need to model the Aggregate Routing Protocol.

Dependencies: `base, extensions.routing`

## Overview

- **Version:** 1.0

## Nodes

### AggregateRoute

- **Description:** Aggregate Protocol with action and BGP communities
- **Label:** Aggregate Routes
- **Icon:** grommet-icons:aggregate
- **Include in Menu:** ❌

#### Attributes

| name | label | kind | optional | default_value | order_weight |
| ---- | ----- | ---- | -------- | ------------- | ------------ |
| discard | Discard | Boolean | True | False | 1275 |
| import\_policies |  | Text | True |  | 1300 |
| export\_policies |  | Text | True |  | 1350 |

#### Relationships

| name | kind | peer | description | order_weight |
| ---- | ---- | ---- | ----------- | ------------ |
| destination | Attribute | IpamPrefix | Destination network for the static route\. | 1200 |
