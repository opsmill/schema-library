# SNMP

This schema extension contains models for SNMP Communities and SNMP Clients. As you can see this extension is not linked to Tenancy or Device, as you could decide to link the Community to different models based on your use case.

Dependencies: `base`

## snmp

- **Version:** 1.0

## Generics

### Community

- **Description:** Generic model for SNMP community configurations.
- **Label:** SNMP Community
- **Icon:** iconoir:community
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | order_weight | optional |
| ---- | ---- | ------------ | -------- |
| name | Text | 1000 |  |
| description | Text | 1100 | True |

#### Relationships

| name | peer | cardinality | kind |
| ---- | ---- | ----------- | ---- |
| clients | SnmpClient | many | Component |

## Nodes

### CommunityV2

- **Description:** SNMP v1/v2c community configuration.
- **Label:** SNMP v1/v2c
- **Icon:** iconoir:community
- **Menu Placement:** SnmpCommunity
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | order_weight | enum |
| ---- | ---- | ------------ | ---- |
| community\_string | Password | 1300 |  |
| access | Text | 1200 | \['Read\-Only', 'Read\-Write'\] |

### CommunityV3

- **Description:** SNMP version 3 configuration with enhanced security.
- **Label:** SNMP v3
- **Icon:** iconoir:community
- **Menu Placement:** SnmpCommunity
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | order_weight | label | enum | optional | choices |
| ---- | ---- | ------------ | ----- | ---- | -------- | ------- |
| username | Text | 1300 |  |  |  | \`\` |
| auth\_protocol | Text | 1400 | Authentication Protocol | \['None', 'MD5', 'SHA'\] |  | \`\` |
| auth\_password | Password | 1500 | Authentication Password |  | True | \`\` |
| privacy\_protocol | Text | 1600 | Privacy Protocol | \['None', 'DES', 'AES'\] |  | \`\` |
| privacy\_password | Password | 1700 | Privacy Password |  | True | \`\` |
| security\_level | Dropdown | 1200 | Security Level |  |  | \`noAuthNoPriv, authNoPriv, authPriv\` |

### Client

- **Description:** Represents an SNMP client that interacts with SNMP Community.
- **Label:** SNMP Client
- **Icon:** ph:user-list-light
- **Menu Placement:** SnmpCommunity
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | order_weight | label | optional |
| ---- | ---- | ------------ | ----- | -------- |
| name | Text | 1000 |  |  |
| client\_description | Text | 1100 | Description | True |

#### Relationships

| name | peer | cardinality | order_weight |
| ---- | ---- | ----------- | ------------ |
| community | SnmpCommunity | many | 1200 |
