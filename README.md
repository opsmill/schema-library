# Schema Library

Welcome to the Schema Library for Infrahub. This repository contains a collection of schemas that are designed to streamline and standardize infrastructure-related data structures.

> [!WARNING]
> 🚧 This project is currently in an experimental phase and is subject to significant changes. The schemas may evolve, and backward compatibility is not guaranteed. Use with caution in production environments, and expect potential breaking changes as we iterate and improve.

## Getting Started

There are various way to consume schema library, you could copy paste some YAML files into your own workspace.

You could also clone the repo and use Infrahub CTL to load the schema.

Follow [this guide](https://docs.infrahub.app/infrahubctl) to install Infrahub CTL.

0. Clone the repository

    ```console
    git clone https://github.com/opsmill/schema-library.git
    ```

1. Create a branch on your Infrahub instance

    ```console
    infrahubctl branch create testing-schema-library
    ```

2. Load the base schema

    _Please note that base schema is a prerequisite to any extension._

    ```console
    infrahubctl schema load --branch testing-schema-library base/
    ```

3. Then pick and load extensions that fit your use case

    ```console
    infrahubctl schema load --branch testing-schema-library extensions/location_minimal
    infrahubctl schema load --branch testing-schema-library extensions/vrf
    infrahubctl schema load --branch testing-schema-library extensions/bgp
    ```

## Contributing

We welcome contributions and feedback. Please open an issue or submit a pull request to suggest improvements or report bugs.
