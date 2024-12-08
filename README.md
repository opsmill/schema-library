# Infrahub Schema Library

Welcome to the Schema Library for Infrahub! This repository offers a collection of schemas designed to streamline and standardize infrastructure-related data structures.

> [!WARNING]
> This project is currently a collection of examples intended to serve as inspiration. Please note that it is in an experimental phase and may undergo significant changes.

## Getting Started

> [!NOTE]
> One of Infrahub’s key strengths is its flexibility. We encourage you to copy any schemas you find useful into your own repository and tailor them to your specific needs, ensuring that your schema aligns perfectly with your requirements.

There are several ways to [load a schema in Infrahub](https://docs.infrahub.app/guides/import-schema):

- Quick View: To take a quick look at a schema, you can use Infrahub CTL. Follow [this guide](https://docs.infrahub.app/infrahubctl) to install Infrahub CTL.

```console
  # Load the base
  infrahubctl schema load base

  # Load an extension
  infrahubctl schema load extensions/location_minimal
```

- Controlled Integration: For a more organized and unified approach to loading schemas, you can connect a Git repository. Follow [this guide](https://docs.infrahub.app/guides/repository) to connect a Git repository.

> [!NOTE]
> Schema extensions don’t specify menu placement, so they will default to the root level of the menu. Follow [this guide](https://docs.infrahub.app/guides/menu) to learn more about menu customization.

## Project Structure

This project is divided into three main parts:

- Base: This is the foundational layer required for any extension. It must be loaded before adding extensions.
- Extensions: Designed to be simple and generic, this section offers various schema components for managing infrastructure. Note that extensions may have dependencies on each other.
- Experimental: This section contains schema components that are not yet fully supported.

## Contributing

We welcome contributions and feedback! Feel free to open an issue or submit a pull request to suggest additions, improvements or to report bugs.

To add a new example, follow these steps:

- Create a directory in `experimental` with the name of the schema example
- Create a `<example_name>.yml` file using the [Infrahub schema format](https://docs.infrahub.app/reference/schema)
- Create a `.metadata.yml` file using the the following example format, modified with a description and needed schema dependencies:

```yaml
---
apiVersion: infrahub.app/v1
kind: Schema
spec:
  description: A text description of the purpose of the schema extension
  dependencies:
    - base
    - extensions.cluster
```

- Run `invoke build` to automatically generate a `README.md` file for the schema extension
- Submit the pull request!
