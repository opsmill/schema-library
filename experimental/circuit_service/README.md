# 🧩 Circuit Service

This schema extension contains model coming on top of circuit to capture a single service shared across multiple circuits.

For example you have a MPLS network supported by a provider connecting multiple locations:

- One single Circuit Service would be needed to store MPLS related information (e.g. service id, provider ...)
- On each site we would create a circuit connecting on one side our device and the Circuit Service on the other side

## Nodes

- CircuitService

## Dependencies

- Circuit
