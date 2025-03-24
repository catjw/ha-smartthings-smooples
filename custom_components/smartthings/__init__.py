"""Support for SmartThings Cloud."""

from homeassistant.components import smartthings


class SmartThingsData(smartthings.SmartThingsData):
    pass

class FullDevice(smartthings.FullDevice):
    pass

async def async_setup_entry(hass: smartthings.HomeAssistant, entry: smartthings.SmartThingsConfigEntry) -> bool:
    """Initialize config entry which represents an installed SmartApp."""
    smartthings.async_setup_entry(hass, entry)
    
    return True
    