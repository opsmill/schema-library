The QinQ extension now loads on Infrahub releases before 1.9. `IpamCVLAN` builds its HFID from its S-VLAN's name,
so `IpamSVLAN` now declares `name` unique; older releases rejected the schema with "HFID of IpamCVLAN refers to peer
IpamSVLAN with a non-unique combination of attributes".
