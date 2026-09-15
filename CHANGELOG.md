# Changelog

This project uses [*towncrier*](https://towncrier.readthedocs.io/) and the changes for the upcoming release can be found in <https://github.com/opsmill/schema-library/tree/main/changelog>.

<!-- towncrier release notes start -->

## [Schema Library - v2.0.0](https://github.com/opsmill/schema-library/tree/v2.0.0) - 2026-09-15

> [!WARNING]
> **Breaking changes in this release**
>
> Attribute and relationship names, types and cardinalities change across `base/dcim.yml`, `base/ipam.yml`, `base/location.yml` and most extensions, so loading v2.0.0 over data created with a v1.x schema requires migrating that data first.
>
> - Plan a migration rather than an in-place upgrade: loading v2.0.0 as-is over a v1.x deployment fails, or silently drops data, on the attributes and relationships listed below.
> - Re-point anything that loaded `extensions/modules` at `extensions/device_module`, and anything that loaded `extensions/topology` at `experimental/topology`. `extensions/users` has no replacement.
> - Update renamed paths: `extensions/sfp` to `extensions/transceiver`, `extensions/dwdm` to `extensions/optical_multiplexer`, and `extensions/firewall_policer` to `experimental/firewall_policer`.
> - Re-case stored values for the enums that became Dropdowns — `BGPSession.session_type` and the SNMP community and client enums — for example `EXTERNAL` to `external` and `Read-Only` to `read_only`.
> - Load either `extensions/location_minimal` or `extensions/location_site`, not both: they define the same `Location.Site` node, and `invoke load-all-schemas` no longer refuses the pair.

### Removed

- `extensions/users` is removed, along with the `UserGroup` and `UserAccount` nodes it defined. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `extensions/modules` is removed. Its generic is superseded by the ready-to-use `Module`/`ModuleType` pair in `extensions/device_module`, and `extensions/modules_linecards` and `extensions/modules_routing_engine` now depend on that extension instead. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `extensions/topology` is removed. `experimental/topology` is now the only topology model in the library, ending the overlap between two competing models. ([#75](https://github.com/opsmill/schema-library/issues/75))

### Added

- Track the commercial terms behind a circuit with `extensions/circuit_contract`, which adds a `DcimCircuitContract` node carrying `contract_start`, `contract_end`, `monthly_cost` and `currency`, related to the circuit it covers. ([#67](https://github.com/opsmill/schema-library/issues/67))
- Model optical transport networks with `experimental/optical_transport`, which covers four layers: the wavelength layer (the ITU-T G.694.1 grid, optical bands, DWDM channels, channel assignments and fiber mappings), the topology layer (logical optical nodes, passive multiplexers and fiber links as a graph), the equipment layer (transponder, amplifier and ROADM modules, ROADM degrees, WSS cross-connects and cable mappings), and the service layer (end-to-end optical services, optical paths and path segments). ([#68](https://github.com/opsmill/schema-library/issues/68))
- Model standalone sites with `extensions/location_site`, which adds a `LocationSite` node (facility, physical address, timezone, status) with no region or country tier above it. It defines the same `Location.Site` node as `extensions/location_minimal`, so load one or the other. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Scope a tenant to the devices, address space and locations it is responsible for with `extensions/tenancy`, promoted out of `experimental/` and rebuilt to wire `Tenant` to `DcimGenericDevice`, `IpamPrefix`, `IpamIPAddress` and `LocationHosting`. It no longer depends on `extensions/circuit`; extending tenancy onto circuits is documented in `tenancy.yml` as a pattern to apply yourself. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Track swappable hardware as installed inventory with `extensions/device_module`, which adds a `DcimModuleBay` node for a physical slot on a device and a ready-to-use `Module`/`ModuleType` pair that installs into a bay. It replaces `extensions/modules`, which shipped only a generic to build on. A module is tracked once it is installed in a bay; spares awaiting installation are not modelled. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Capture circuit bandwidth, endpoint sides, VRF uniqueness enforcement, IP address lifecycle and SNMP scoping with the new `DcimCircuit.commit_rate`, `DcimCircuitEndpoint.side`, `IpamVRF.enforce_unique`, `IpamIPAddress.status` and `role`, `SnmpCommunity.devices` and `SnmpClient.ip_addresses` attributes and relationships. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Model power supplies alongside other modules with `extensions/device_module_psu`, which adds `DcimPSUModule` and `DcimPSUModuleType`, carrying `wattage` (Number) and `hot_swappable` (Boolean) on the type. It depends on `extensions/device_module`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Record which registry assigned a block of address space by loading `extensions/ipam_aggregate`, which adds an `Aggregate` node for top-level IPv4/IPv6 blocks and an `RIR` node carrying a `private` flag. Previously top-level space could only be marked with a role on a generic prefix. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Model racks without adopting a full location hierarchy by loading `extensions/rack`, which takes `LocationRack` out of `extensions/location_minimal` and relates it to a site through an explicit `site`/`racks` relationship rather than hierarchical nesting. The rack gains `status`, `serial_number` and `asset_tag` attributes it did not have before. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Import the ports a module type declares — what NetBox lists under `interfaces`, `console-ports` and `power-ports` — with `extensions/module_port`. A `DcimModulePort` is a declaration parented by the module, carrying `name`, `category` (`interface`, `console`, `power`, `front` or `rear`), `port_type`, `mgmt_only` and `maximum_draw`, gathered in one typed `DcimGenericModule.ports` collection rather than five parallel relationships. Port names keep NetBox's `{module}` token verbatim, because a template is not bound to a bay; resolving the token and creating the real device interfaces is a generator step once the module is installed. ([#76](https://github.com/opsmill/schema-library/issues/76))
- Carry NetBox's free-text bay label and a module's weight without losing either to rounding: `DcimModuleBay.bay_label` keeps the label distinct from the auto-populated, title-cased `label` attribute, and `DcimGenericModuleType.weight_grams` records a weight in grams, since integer kilograms round a transceiver or supervisor to `0`. ([#76](https://github.com/opsmill/schema-library/issues/76))

### Changed

- Every node and generic in the library declares a single `display_label` string instead of a `display_labels` list, matching the current Infrahub schema format. ([#62](https://github.com/opsmill/schema-library/issues/62))
- Aggregated interfaces are modelled consistently across extensions: `extensions/lag` adds `bundle_number`, renames `lag_members` to `bundle_members` and gives both sides the `interface__bundle` identifier, and `extensions/mlag` drops its own `mlag_id` attribute. In `extensions/transceiver`, the transceiver's peer moves from the `DcimInterface` generic to `InterfacePhysical`, and both sides share the `sfp__interface` identifier. ([#66](https://github.com/opsmill/schema-library/issues/66))
- Model QinQ with dedicated node types instead of a role patched onto a generic VLAN: `extensions/qinq` is rebuilt around `IpamSVLAN` and `IpamCVLAN` on a new `IpamGenericVLAN` generic in `extensions/vlan`, replacing the `qinq_role` Dropdown on `IpamVLAN`. A `CVLAN`'s name is computed from its parent `SVLAN` and VLAN ID, and the file is renamed `qinq.yaml` to `qinq.yml`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `extensions/hosting_cluster` renames `cluster_type` to `technology` and replaces the cloud-specific `aws` and `gcp` choices with a single `public_cloud`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `extensions/firewall_policer` moves to `experimental/firewall_policer`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Set an MTU that reflects the IP payload rather than the full Ethernet frame: `DcimInterface.mtu` changes its default from `1514`, the full Ethernet frame size, to `1500`, and becomes optional. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `IpamL2Domain` is replaced by `IpamVLANGroup`, scoped to a location through the new `IpamVLANGroupScope` mixin in the same way `extensions/ipam_aggregate` scopes to an RIR. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `BGPSession.session_type` and the SNMP community and client enums (`SnmpCommunityV2.access`, `SnmpCommunityV3.auth_protocol` and `privacy_protocol`) move from `kind: Text` with an `enum:` list to `kind: Dropdown`. Their stored values change case with the move, for example `EXTERNAL` to `external` and `Read-Only` to `read_only`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `DcimCircuitEndpoint.name` is now computed from the circuit ID and the side, replacing free text. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Import and export more than one route target per VRF: `IpamVRF.import_rt` and `export_rt` move from `cardinality: one` to `many`, and the corresponding `IpamRouteTarget` relationship splits into `import_vrf` and `export_vrf`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `VRRPGroup.group` is renamed to `vrid` and retyped from `Text` to `Number`, and `VRRPGroup.ip_address` becomes `ip_addresses`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `DcimInterface.role` drops the `lag` choice, which `InterfaceLag` already models, and renames `cust` to `customer`. `DcimInterface.status` drops `deleted` and `outage` and is now mandatory. ([#75](https://github.com/opsmill/schema-library/issues/75))
- The `extensions/location_minimal` hierarchy changes from `Country → Metro → Site` to `Region → Country → Metro → Site`, adding a region tier above country. `LocationRack` moves out to `extensions/rack`, and `Site.facility_id` is renamed to `facility`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `LocationGeneric` and `LocationHosting` drop the `shortname` attribute, and their `human_friendly_id` switches to `name`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `DcimCircuit.circuit_type` replaces the `upstream` choice with `internet_access` and adds `point_to_point`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- A circuit's location is now recorded on its endpoints rather than twice: `DcimCircuit` drops its own `location` relationship, and `DcimCircuitEndpoint.location` remains the place a circuit is tied to a `LocationHosting`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- Attach a prefix to whatever owns it through one `scope` relationship: `IpamPrefix` drops its separate `organization`, `location` and `gateway` relationships in favour of `scope` (`IpamPrefixScope`). Its `role` choices are fully replaced, from `loopback`, `management`, `public`, `server`, `supernet`, `technical` and `loopback-vtep` to `management`, `link`, `customer` and `backbone`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `DcimDevice.status` drops the `drained` choice and adds `reserved` and `deprecated`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `DcimModuleBay.position` becomes `Text` rather than a `Number` with `min_value: 1`, because bay positions in the NetBox device-type library are free-form. An Arista DCS-7508N alone uses `F1`–`F6` and `PSU-1`–`PSU-8` alongside `1`–`10`, and an A9K-AC-PEM-V3 starts its bays at `0`. ([#76](https://github.com/opsmill/schema-library/issues/76))
- Import a line card as a reusable blueprint rather than as an installed card: `DeviceLinecard` in `experimental/modules_linecards` now enables `generate_template`, and its `slot` becomes optional, since a NetBox module type describes a model and carries no slot. ([#76](https://github.com/opsmill/schema-library/issues/76))
- `extensions/sfp` is renamed to `extensions/transceiver`, broadening its scope from SFP alone to pluggable transceivers across form factors — SFP, SFP+, QSFP, QSFP28, QSFP-DD, OSFP, CFP and XFP. `extensions/dwdm` is renamed to `extensions/optical_multiplexer`. ([#89](https://github.com/opsmill/schema-library/issues/89))
- `invoke load-all-schemas` no longer refuses mutually exclusive extension pairs. The `exclusive_with` key is removed from `.metadata.yml`, so the overlap between `extensions/rack` and `experimental/location_extended`, and between `extensions/location_minimal` and `extensions/location_site`, is now described in each extension's description rather than enforced at load time. ([#89](https://github.com/opsmill/schema-library/issues/89))

### Fixed

- The Infrahub sidebar no longer shows two top-level entries pointing at the same records. `DcimGenericDevice`, `DcimChannelMapping` and `DcimOpticalDevice` are abstract generics whose concrete descendants already render their own top-level entries, so all three are now hidden from the auto-generated menu, in line with the other abstract generics in `base/dcim.yml`. ([#73](https://github.com/opsmill/schema-library/issues/73))
- `experimental/security` loads again. It referenced kinds from the old `Infra` namespace, which had been renamed to `Dcim` for devices, interfaces and endpoints and `Ipam` for addresses and prefixes, so the load aborted with `SecurityFirewall Unable to find the generic InfraGenericDevice`. `SecurityFirewall` also now inherits `DcimPhysicalDevice`, matching `DcimDevice`, which the deployed schema already expected. ([#74](https://github.com/opsmill/schema-library/issues/74))
- `DcimCircuit.enpoints` is corrected to `endpoints`. ([#75](https://github.com/opsmill/schema-library/issues/75))
- `IpamIPAddress.interface` and `InterfaceLayer3.ip_addresses` now carry a matching `identifier`, so both sides resolve as one relationship instead of being treated as unrelated. ([#75](https://github.com/opsmill/schema-library/issues/75))
- A BGP session's routing policies are no longer conflated with a peer group's. `RoutingBGPSession.import_routing_policies` and `export_routing_policies` pointed at the generic `RoutingPolicy` peer and reused the `bgp__import_policies` and `bgp__export_policies` identifiers already used by `RoutingBGPPeerGroup`; both now point at `RoutingPolicyBGP` and use distinct identifiers. ([#75](https://github.com/opsmill/schema-library/issues/75))

### Housekeeping

- The changelog is now assembled from news fragments with [towncrier](https://towncrier.readthedocs.io/).
  Add a file under `changelog/` named `<id>.<type>.md` describing your change, where `<type>` is one of
  `security`, `removed`, `deprecated`, `added`, `changed`, `fixed` or `housekeeping`. A CI check fails a
  pull request that carries none, unless it is labelled `ci/skip-changelog`. Releases up to and including
  v1.4.11 are not back-filled.
