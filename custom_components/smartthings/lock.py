"""Support for locks through the SmartThings cloud API."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import lock

from . import SmartThingsConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add locks for a config entry."""
    await lock.async_setup_entry(hass, entry, async_add_entities)
