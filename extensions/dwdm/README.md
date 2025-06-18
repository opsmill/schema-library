# DWDM

This schema extension contains models for OADM (Optical Add Drop Multiplexer) supporting various WDM (Wavelength Division Multiplexing) technologies such as DWDM (Dense Wavelength Division Multiplexing) or CWDM (Coarse Wavelength Division Multiplexing). With some vendors, the tunable optics are not configured via the channel number but via the wavelength and/or the frequency. This model provides a unique entry in Infrahub for those.

Dependencies: `base, extensions/sfp`

## dwdm

- **Version:** 1.0

## Generics

### GenericOadmInterface

- **Label:** Optical Multiplexer Interfaces
- **Icon:** mdi:ethernet
- **Menu Placement:** DcimOpticalMultiplexer
- **Include in Menu:** ❌

#### Attributes

| name | kind | order_weight | optional | choices |
| ---- | ---- | ------------ | -------- | ------- |
| name | Text | 1000 |  | \`\` |
| description | Text | 2000 | True | \`\` |
| connector\_type | Dropdown | 1100 |  | \`FC, LC, LC\_PC, LC\_UPC, LC\_APC, LSH, LSH\_PC, LSH\_UPC, LSH\_APC, LX\_5, LX\_5\_PC, LX\_5\_UPC, LX\_5\_APC, MPO, MTRJ, SC, SC\_PC, SC\_UPC, SC\_APC, ST, CS, SN, SMA\_905, SMA\_906, URM\_P2\` |

## Nodes

### OpticalMultiplexer

- **Description:** An OADM (Optical Add Drop Multiplexer) supporting various WDM (Wavelength Division Multiplexing) technologies.
- **Label:** Optical Multiplexer
- **Icon:** mdi:transit-connection-variant
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**

#### Attributes

| name | kind | unique | order_weight | description | optional | choices | default_value |
| ---- | ---- | ------ | ------------ | ----------- | -------- | ------- | ------------- |
| name | Text | True | 1000 |  |  | \`\` |  |
| wdm\_type | Dropdown |  | 1110 | Type of WDM \(e\.g CWDM\. DWDM\) | False | \`cwdm, dwdm\` | dwdm |
| description | Text |  | 2000 |  | True | \`\` |  |

#### Relationships

| name | peer | identifier | optional | cardinality | kind |
| ---- | ---- | ---------- | -------- | ----------- | ---- |
| front\_interfaces | DcimOadmFrontInterface | front\_interfaces | True | many | Component |
| rear\_interface | DcimOadmRearInterface | rear\_interfaces | True | one | Component |

### OadmFrontInterface

- **Label:** Optical Multiplexer Front Interfaces
- **Menu Placement:** DcimGenericOadmInterface
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**optical_multiplexer__name__value, name__value
- **Uniqueness Constraints:**optical_multiplexer + name__value

#### Relationships

| name | peer | order_weight | identifier | optional | cardinality | kind |
| ---- | ---- | ------------ | ---------- | -------- | ----------- | ---- |
| optical\_multiplexer | DcimOpticalMultiplexer | 900 | front\_interfaces | False | one | Parent |
| channels | DcimWdmChannel | 1200 |  | True | many | Attribute |

### OadmRearInterface

- **Label:** Optical Multiplexer Rear Interfaces
- **Menu Placement:** DcimGenericOadmInterface
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**optical_multiplexer__name__value, name__value
- **Uniqueness Constraints:**optical_multiplexer + name__value

#### Relationships

| name | peer | order_weight | identifier | optional | cardinality | kind |
| ---- | ---- | ------------ | ---------- | -------- | ----------- | ---- |
| optical\_multiplexer | DcimOpticalMultiplexer | 900 | rear\_interface | False | one | Parent |

### WdmChannel

- **Description:** A WDM channel with its wavelength and frequency.
- **Label:** WDM Channel
- **Icon:** game-icons:laser-warning
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**wdm_type__value, channel__value
- **Uniqueness Constraints:**wdm_type__value + channel__value + wavelength__value + frequency__value, wdm_type__value + channel__value

#### Attributes

| name | kind | description | order_weight | optional | choices | default_value | label |
| ---- | ---- | ----------- | ------------ | -------- | ------- | ------------- | ----- |
| channel | Number | WDM channel number\. |  |  | \`\` |  |  |
| wdm\_type | Dropdown | Type of WDM \(e\.g CWDM\. DWDM\) | 1110 | False | \`cwdm, dwdm\` | dwdm |  |
| wavelength | Text | Wavelength of the channel in nm\. |  |  | \`\` |  | Wavelength \(nm\) |
| frequency | Text | Frequency of the channel in GHz\. |  |  | \`\` |  | Frequency \(GHz\) |

### WdmSFP

- **Description:** SFP with configuration for Wavelength Division Multiplexing.
- **Label:** WDM SFP
- **Icon:** mdi:laser-pointer
- **Menu Placement:** DcimGenericSFP
- **Include in Menu:** ❌

#### Attributes

| name | kind | description | order_weight | optional | choices | default_value |
| ---- | ---- | ----------- | ------------ | -------- | ------- | ------------- |
| wdm\_type | Dropdown | Type of WDM \(e\.g CWDM\. DWDM\) | 1110 | False | \`cwdm, dwdm\` | dwdm |

#### Relationships

| name | label | peer | kind | cardinality | optional | order_weight |
| ---- | ----- | ---- | ---- | ----------- | -------- | ------------ |
| wdm\_channel | WDM Channel | DcimWdmChannel | Attribute | one | False | 1150 |
