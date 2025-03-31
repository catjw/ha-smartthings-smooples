"""Support for SmartThings Cloud."""

from dataclasses import dataclass
from homeassistant.components import smartthings
from pysmartthings import (
    Attribute,
    Capability,
    Device,
    DeviceEvent,
    Scene,
    SmartThings,
    SmartThingsAuthenticationFailedError,
    SmartThingsSinkError,
    Status,
)

# @dataclass
# class FullDevice(smartthings.FullDevice):
#     """Define an object to hold device data."""

#     device: Device
#     status: dict[str, dict[Capability | str, dict[Attribute | str, Status]]]

# @dataclass
# class SmartThingsData(smartthings.SmartThingsData):
#     """Define an object to hold SmartThings data."""

#     devices: dict[str, FullDevice]
#     scenes: dict[str, Scene]
#     client: SmartThings

async def async_setup_entry(hass: smartthings.HomeAssistant, entry: smartthings.SmartThingsConfigEntry) -> bool:
    """Initialize config entry which represents an installed SmartApp."""
    return smartthings.async_setup_entry(hass, entry)
    
    # return True
    
# for i in smartthings.__all__:
#     setattr(SmartThingsData, i, getattr(smartthings, i))
#     setattr(FullDevice, i, getattr(smartthings, i))