# dwdm

This schema extension contains models for OADM (Optical Add Drop Multiplexer) supporting various WDM (Wavelength Division Multiplexing) technologies such as DWDM (Dense Wavelength Division Multiplexing) or CWDM (Coarse Wavelength Division Multiplexing).
With some vendors, the tunable optics are not configured via the channel number but via the wavelength and/or the frequency. This model provides a unique entry in Infrahub for those.


## Generics

- GenericOadmInterface

## Nodes

- OpticalMultiplexer
- OadmFrontInterface
- OadmRearInterface
- WdmChannel
- WdmSFP

## Dependencies

- base
- extensions.sfp
