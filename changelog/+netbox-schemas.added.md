Added nine schemas under `netbox/` that mirror the NetBox 4.7 data model, one for each section of the
NetBox navigation menu: `netbox_organization`, `netbox_devices`, `netbox_racks`, `netbox_connections`,
`netbox_power`, `netbox_cooling`, `netbox_ipam`, `netbox_circuits` and `netbox_vpn`. A team that runs
NetBox can load only the sections it uses and import its NetBox data into nodes of the `Netbox`
namespace. `netbox_organization` and `netbox_devices` are loaded first. The other schemas require only
these two, except `netbox_power` and `netbox_cooling`, which also require `netbox_racks`, and
`netbox_vpn`, which also requires `netbox_ipam`. NetBox device type component templates map to Infrahub
object templates, and each NetBox VRF is an Infrahub IP namespace. A menu file for each schema, under
`menus/netbox/`, adds the section of that schema to the Infrahub sidebar, in the order of the NetBox
navigation menu. See `netbox/README.md` for the load order, the menus and the table-by-table mapping.
