"""Support for sensors through the SmartThings cloud API."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import SmartThingsConfigEntry

from homeassistant.components.smartthings import sensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add sensors for a config entry."""
    await sensor.async_setup_entry(hass, entry, async_add_entities)
    