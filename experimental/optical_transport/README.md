# optical_transport

Optical transport network schemas for DWDM/WDM systems (ADVA FSP 3000 and similar platforms).

## Overview

This experimental extension provides a comprehensive model for optical transport networks,
covering four layers:

1. **Wavelength Layer** (`wavelength.yml`) - ITU-T G.694.1 grid, optical bands, DWDM channels, channel assignments and fiber mappings
2. **Topology Layer** (`topology.yml`) - Logical optical nodes, passive multiplexers, fiber links (graph model)
3. **Equipment Layer** (`equipment.yml`) - Transponder/amplifier/ROADM modules, ROADM degrees, WSS cross-connects, cable mappings
4. **Service Layer** (`service.yml`) - End-to-end optical services, optical paths, path segments

## Dependencies

- `extensions/modules/modules.yml` (DeviceGenericModule, DeviceGenericModuleType)
- `extensions/cable/cable.yml` (DcimCable)
- `base/dcim.yml` (DcimGenericDevice, DcimPhysicalDevice, DcimEndpoint, DcimConnector)

## Relationship to extensions/dwdm

This schema provides a richer DWDM channel model (`DcimDWDMChannel`) with ITU grid hierarchy
(Grid -> Band -> Channel) compared to the simpler `DcimWdmChannel` in `extensions/dwdm/`.
They are **not** designed to be loaded together. If you need the full optical transport model,
use this extension instead of `extensions/dwdm/`.

## Status

Experimental - API may change. Originally developed for ADVA FSP 3000 optical transport networks.
