"""Time platform for SmartThings."""

from datetime import time

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice
from . import SmartThingsConfigEntry

from homeassistant.components.smartthings import time as st_time


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add time entities for a config entry."""
    entry_data = entry.runtime_data
    async_add_entities(
        st_time.SmartThingsDnDTime(entry_data.client, device, description)
        for device in entry_data.devices.values()
        if st_time.Capability.CUSTOM_DO_NOT_DISTURB_MODE in device.status.get(st_time.MAIN, {})
        for description in st_time.DND_ENTITIES
    )