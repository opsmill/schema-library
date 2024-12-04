# 🧩 Routing Policies BGP

This extension is using the Routing Policies extensions and the Routing BGP one together.

## Generics


## Nodes

- RoutingPolicyBGP

## Extension

- Removes Attributes import_policies and export_policies from BGPPeerGroup and BGPSession
- Add Relationships import_routing_policies and export_routing_policies on BGPPeerGroup and BGPSession

## Dependencies

- Base (need by BGP and RoutingPolcies)
- Routing (need by BGP)
- RoutingPolcies
- BGP
