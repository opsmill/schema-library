# NetBox

Schemas that mirror the [NetBox](https://netboxlabs.com/docs/netbox/) 4.7 data model, so that a team that runs NetBox can load the same data model into Infrahub and import its NetBox data, one section of the NetBox navigation menu at a time.

The mapping is based on the NetBox 4.7.2 database tables and the [NetBox model documentation](https://netboxlabs.com/docs/netbox/models/dcim/device/). Every node uses the `Netbox` namespace, for example `NetboxDevice` or `NetboxPrefix`, so these schemas can be loaded in the same Infrahub instance as the rest of the library without kind conflicts. They do not depend on the `base` schema.

## Load order of the NetBox schemas

Each schema holds the nodes of one section of the NetBox navigation menu. Load only the schemas you need, in this order:

| Schema | Requires | NetBox menu section |
| ------ | -------- | ------------------- |
| `netbox/netbox_organization` | nothing | [Organization](https://netboxlabs.com/docs/netbox/models/dcim/site/): regions, site groups, sites, locations, tenants and contacts |
| `netbox/netbox_devices` | `netbox_organization` | [Devices](https://netboxlabs.com/docs/netbox/models/dcim/device/): devices, modules, device types, module types, manufacturers, device components, inventory items and MAC addresses |
| `netbox/netbox_racks` | `netbox_organization`, `netbox_devices` | [Racks](https://netboxlabs.com/docs/netbox/models/dcim/rack/): racks, reservations, rack groups, rack roles and rack types |
| `netbox/netbox_connections` | `netbox_organization`, `netbox_devices` | [Connections](https://netboxlabs.com/docs/netbox/models/dcim/cable/): cables and cable bundles |
| `netbox/netbox_power` | `netbox_organization`, `netbox_devices`, `netbox_racks` | [Power](https://netboxlabs.com/docs/netbox/models/dcim/powerfeed/): power panels and power feeds |
| `netbox/netbox_cooling` | `netbox_organization`, `netbox_devices`, `netbox_racks` | [Cooling](https://netboxlabs.com/docs/netbox/models/dcim/coolingsource/): cooling sources and cooling feeds |
| `netbox/netbox_ipam` | `netbox_organization`, `netbox_devices` | [IPAM](https://netboxlabs.com/docs/netbox/models/ipam/prefix/) |
| `netbox/netbox_circuits` | `netbox_organization`, `netbox_devices` | [Circuits](https://netboxlabs.com/docs/netbox/models/circuits/circuit/) |
| `netbox/netbox_vpn` | `netbox_organization`, `netbox_devices`, `netbox_ipam` | [VPN](https://netboxlabs.com/docs/netbox/models/vpn/tunnel/) |

```bash
infrahubctl schema load netbox/netbox_organization
infrahubctl schema load netbox/netbox_devices
infrahubctl schema load netbox/netbox_racks
infrahubctl schema load netbox/netbox_connections
infrahubctl schema load netbox/netbox_power
infrahubctl schema load netbox/netbox_cooling
infrahubctl schema load netbox/netbox_ipam
infrahubctl schema load netbox/netbox_circuits
infrahubctl schema load netbox/netbox_vpn
```

Any order in which each schema comes after the schemas it requires also works. The optional schemas complete each other whichever is loaded first:

- `netbox_connections` adds the cable fields to interfaces, ports, power feeds and circuit terminations, whether `netbox_power` and `netbox_circuits` are loaded before or after it.
- When `netbox_racks` and `netbox_ipam` are both loaded, a rack or a rack group can scope a VLAN group.
- When `netbox_circuits` and `netbox_ipam` are both loaded, providers have an ASNs relationship.

To load all nine schemas with one command, pass the `netbox` folder. `infrahubctl` sends every schema file in the folder in one request, so the order of the files does not matter:

```bash
infrahubctl schema load netbox
```

The NetBox apps core, extras, users, virtualization and wireless are not mapped.

## Sidebar menu grouped like NetBox

`menus/netbox/` holds one menu file for each NetBox schema. The menu files are outside the `netbox` folder, because `infrahubctl schema load netbox` reads every YAML file in that folder as a schema. Each file adds the section of its schema to the Infrahub sidebar, so that together they arrange the sidebar like the NetBox navigation menu: Organization, Racks, Devices, Connections, IPAM, VPN, Circuits, Power and Cooling. The sections keep this order whatever order the files are loaded in. The IPAM groups are placed in the IPAM section that Infrahub already provides, after its IP Prefixes, IP Addresses and Namespaces views. Two groups differ from NetBox:

- "IP Addresses and Ranges" is the NetBox "IP Addresses" group, renamed so that it does not repeat the Infrahub IP Addresses view next to it.
- "FHRP and Services" is the NetBox "Other" group.

Load the menu files of the schemas you loaded, after the schemas:

```bash
infrahubctl menu load menus/netbox/netbox_organization.yml menus/netbox/netbox_devices.yml \
  menus/netbox/netbox_racks.yml menus/netbox/netbox_connections.yml menus/netbox/netbox_power.yml \
  menus/netbox/netbox_cooling.yml menus/netbox/netbox_ipam.yml menus/netbox/netbox_circuits.yml \
  menus/netbox/netbox_vpn.yml
```

When you loaded all nine schemas, load all the menu files by passing their folder:

```bash
infrahubctl menu load menus/netbox
```

Do not load the menu of a schema you did not load: Infrahub does not check that a menu item's kind exists, so the item would link to a page that does not exist.

Each menu item that opens a list has the namespace and name of its node, for example namespace `Netbox` and name `Device` for `NetboxDevice`. Infrahub leaves a node out of its generated menu when a menu item with the same namespace and name exists. So the nodes keep `include_in_menu: true` without being listed twice, and they still appear in the generated menu when the menu files are not loaded.

## Why the organization and devices schemas come first

NetBox objects refer to each other across menu sections: a device has a primary IP address, an IP address is assigned to an interface, and a circuit termination is cabled to an interface. An Infrahub schema can only refer to nodes that are already loaded, and Infrahub cannot add a generic to a node after the node is loaded. So:

- `netbox_organization` defines the generics that every other NetBox schema inherits: `NetboxGeneric` (description, comments and tags), `NetboxTenantAssignable` (tenant) and `NetboxContactAssignable` (contact assignments). It also defines empty generics that the regions, site groups, sites and locations inherit and that later schemas complete, for example `NetboxPrefixScope`, which `netbox_ipam` completes with the prefixes relationship.
- `netbox_devices` defines the empty generics that the device components inherit, for example `NetboxCabledObject`, which `netbox_connections` completes with the cable fields.
- Each later schema adds its relationships to the nodes of the earlier schemas. For example, `netbox_racks` adds the rack, position and rack face fields to `NetboxDevice`, and `netbox_ipam` adds the primary IP addresses to `NetboxDevice`.

`netbox_racks` comes after `netbox_devices` because a NetBox rack type has a manufacturer, which NetBox lists in the Devices section. A team that does not record racks can load the devices without the racks.

## How NetBox concepts map to Infrahub

- **Device component templates.** NetBox device types hold component templates (`dcim_interfacetemplate` and the other `dcim_*template` tables). In Infrahub, `NetboxDevice` generates an object template, and Infrahub also generates a template for each component kind, for example `TemplateNetboxInterface`. Create a device template with its components, then create devices from it. Module type component templates and front-to-rear port template mappings have no equivalent.
- **VRFs.** A NetBox VRF is an Infrahub IP namespace: `NetboxVRF` inherits `BuiltinIPNamespace`, and the VRF of a prefix or IP address is its `ip_namespace`. Infrahub builds a separate prefix hierarchy for each VRF. Prefixes and IP addresses in the NetBox global table go into the Infrahub `default` namespace.
- **Cable terminations.** NetBox stores the cable, the cable end (A or B) and the connector position on each port, interface, power feed and circuit termination. These objects inherit `NetboxCabledObject` from `netbox_devices`, and `netbox_connections` adds the same fields to it. `NetboxCable.terminations` lists the objects at both ends.
- **Polymorphic relationships.** Where a NetBox field can point to several models (a generic foreign key), the Infrahub relationship points to a generic, for example the scope of a prefix (`NetboxPrefixScope`) or the object an IP address is assigned to (`NetboxIPAddressAssignable`).
- **Choices.** Status, mode and other fields with a fixed list of NetBox values are Dropdowns with the NetBox values, labels, descriptions and colors. Type fields with more than 40 NetBox values (interface, power port, power outlet, front port and rear port types) are Text, holding the NetBox value, for example `1000base-t`, so that a new NetBox type does not block an import. If you added choices with the NetBox `FIELD_CHOICES` setting, add them to the Dropdowns too.
- **Labels.** The NetBox `label` field of components and cables is `physical_label`, because Infrahub fills an attribute named `label` from the name when it is empty.
- **Decimal values.** Infrahub has no decimal attribute kind. Weights are stored in grams, cable lengths in centimeters, circuit distances in meters, diameters in millimeters, flow rates in liters per minute and cooling capacities in watts, as whole numbers. Latitude and longitude are text. Rack heights and positions are whole rack units.
- **Names that NetBox makes unique within a parent.** An Infrahub uniqueness constraint can only include mandatory relationships. Location, rack, VLAN, VLAN group, module bay and inventory item names are not unique in Infrahub. Tenant, contact group, region, site group, device role, platform and module bay type names are unique in Infrahub.
- **Device names and human-friendly IDs.** Device names are mandatory and unique in Infrahub, while NetBox makes them optional and unique only within a site and tenant. Infrahub requires the attributes of a human-friendly ID that go through a peer to be unique on that peer, so this is what gives devices a human-friendly ID (their name) and gives interfaces, other device components and virtual device contexts the ID [device name, name]. An object file can then refer to an interface as `["leaf1", "Ethernet1"]`. Import a NetBox device without a name, or with a name another device uses, after giving it a unique name.
- **Platform and tenant of devices.** Every device must have a platform and a tenant in Infrahub, while NetBox allows a device without them. Before you import a NetBox device that has no platform or tenant, give it one. `NetboxDevice` redefines the `tenant` relationship that it inherits from `NetboxTenantAssignable` as mandatory, with the same peer and identifier, so the assigned objects of a tenant still include its devices. A device template can set the platform and the tenant of the devices created from it.
- **Trees.** Regions, site groups, locations, tenant groups, contact groups, device roles, platforms and inventory items each inherit their own hierarchical generic, for example `NetboxRegionHierarchy`. Infrahub then adds the `parent`, `children`, `ancestors` and `descendants` fields, so a query can list every region below Europe, or every location in a building. The `parent` and `children` of each tree point to its hierarchical generic, not to the node itself, because the Infrahub 1.11 web interface stops responding on the list page of a node that is its own parent. Each generic has only one node, so a region can still only have a region as its parent.
- **Artifacts.** `NetboxDevice` inherits `CoreArtifactTarget`, so device configurations can be generated as Infrahub artifacts.
- **Not mapped.** Cable paths, the counters and cache columns that NetBox computes, owners, custom fields, and the fields that refer to the apps that are not mapped (clusters, wireless networks and links, configuration templates, VM interfaces).

## NetBox tables without a node of the same name

| NetBox table | In Infrahub |
| ------------ | ----------- |
| `dcim_*template`, `dcim_porttemplatemapping`, `dcim_modulebaytemplate_module_bay_types` | Object templates of `NetboxDevice` and its components |
| `dcim_cabletermination` | Fields that `netbox_connections` adds to `NetboxCabledObject` |
| `dcim_cablepath` | Not mapped: NetBox computes it |
| `dcim_interface_wireless_lans` | Not mapped: wireless app |
| `circuits_provider_asns`, `dcim_site_asns` | `asns` relationship of `NetboxASNAssignable` |
| `dcim_interface_tagged_vlans` | `NetboxInterface.tagged_vlans` |
| `dcim_interface_vdcs` | `NetboxInterface.virtual_device_contexts` |
| `dcim_modulebay_module_bay_types`, `dcim_moduletype_module_bay_types` | `module_bay_types` relationships |
| `ipam_service_ipaddresses` | `NetboxService.ip_addresses` |
| `ipam_vrf_import_targets`, `ipam_vrf_export_targets` | `NetboxVRF.import_targets`, `NetboxVRF.export_targets` |
| `vpn_l2vpn_import_targets`, `vpn_l2vpn_export_targets` | `NetboxL2VPN.import_targets`, `NetboxL2VPN.export_targets` |
| `tenancy_contact_groups` | `NetboxContact.groups` |
| `vpn_ikepolicy_proposals`, `vpn_ipsecpolicy_proposals` | `proposals` relationships |

Every other table of the NetBox dcim, tenancy, ipam, circuits and vpn apps maps to the node of the same name, for example `dcim_device` to `NetboxDevice`. The only renamed model is `ipam_role`, which maps to `NetboxIPAMRole`.
