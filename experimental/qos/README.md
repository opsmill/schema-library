## Quality of Service (QoS)

This schema extension contains models for Quality of Service (QoS)

- **Dependencies:** `base`
- **Version:** 1.0

### Nodes

#### ForwardingClass

- **Description:** Represents a forwarding class in QoS with distinct loss priorities.
- **Label:** Forwarding Class
- **Menu Placement:** QosClassOfService
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | description | unique | order_weight | optional |
| ---- | ---- | ----------- | ------ | ------------ | -------- |
| name | Text | Name of the forwarding class\. | True | 1000 |  |
| high\_loss\_priority\_code | List | List of code points for high loss priority\. |  | 1200 | True |
| low\_loss\_priority\_code | List | List of code points for low loss priority\. |  | 1300 | True |

#### ClassOfService

- **Description:** Defines a Class of Service configuration.
- **Label:** Class of Service
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | description | unique | order_weight |
| ---- | ---- | ----------- | ------ | ------------ |
| name | Text | Name of the Class of Service\. | True | 1000 |

#### Relationships

| name | peer | description | cardinality | optional | order_weight |
| ---- | ---- | ----------- | ----------- | -------- | ------------ |
| traffic\_control\_profiles | QosTrafficControlProfile | List of traffic control profiles\. | many | True | 1200 |

#### TrafficControlProfile

- **Description:** Defines a traffic control profile with an active/inactive state.
- **Label:** Traffic Control Profile
- **Menu Placement:** QosClassOfService
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | description | unique | order_weight | choices | default_value |
| ---- | ---- | ----------- | ------ | ------------ | ------- | ------------- |
| name | Text | Name of the traffic control profile\. | True | 1000 | \`\` |  |
| status | Dropdown | Status of the traffic control profile \(active/inactive\)\. |  | 1200 | \`active, inactive\` | inactive |

#### Classifier

- **Description:** Represents a classifier mapping DSCP or EXP values to forwarding classes.
- **Label:** Classifier
- **Menu Placement:** QosClassOfService
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | description | unique | order_weight | choices |
| ---- | ---- | ----------- | ------ | ------------ | ------- |
| name | Text | Name of the classifier\. | True | 1000 | \`\` |
| classifier\_type | Dropdown | Type of classifier \(DSCP, EXP, etc\.\)\. |  | 1200 | \`dscp, exp, dscp\-ipv6\` |

#### Relationships

| name | peer | description | cardinality | optional | order_weight |
| ---- | ---- | ----------- | ----------- | -------- | ------------ |
| forwarding\_classes | QosForwardingClass | List of forwarding classes defined in the classifier\. | many | True | 1300 |

#### Scheduler

- **Description:** Represents a scheduler configuration.
- **Label:** Scheduler
- **Menu Placement:** QosClassOfService
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | description | unique | order_weight | label | choices | optional |
| ---- | ---- | ----------- | ------ | ------------ | ----- | ------- | -------- |
| name | Text | Name of the scheduler\. | True | 1000 |  | \`\` |  |
| transmit\_rate | Number | Transmit rate in percentage\. |  | 1200 | Transmit Rate \(%\) | \`\` |  |
| buffer\_size | Number | Buffer size in percentage\. |  | 1300 | Buffer Size \(%\) | \`\` |  |
| priority | Dropdown | Priority of the scheduler\. |  | 1400 |  | \`low, high, strict\-high\` | True |
| excess\_priority | Dropdown | Excess priority when applicable\. |  | 1500 |  | \`low, high\` | True |

#### SchedulerMap

- **Description:** Defines mappings of schedulers to forwarding classes.
- **Label:** Scheduler Map
- **Menu Placement:** QosClassOfService
- **Include in Menu:** ❌

#### Ordering and Constraints

- **Order By:**name__value
- **Uniqueness Constraints:**name__value

##### Attributes

| name | kind | description | unique | order_weight |
| ---- | ---- | ----------- | ------ | ------------ |
| name | Text | Name of the scheduler map\. | True | 1000 |

#### Relationships

| name | peer | description | cardinality | optional | order_weight |
| ---- | ---- | ----------- | ----------- | -------- | ------------ |
| schedulers | QosScheduler | List of schedulers defined in the map\. | many | True | 1200 |
| forwarding\_classes | QosForwardingClass | List of forwarding classes associated with schedulers\. | many | True | 1300 |
