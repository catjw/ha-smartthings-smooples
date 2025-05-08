"""Support for number entities through the SmartThings cloud API."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import number

from . import SmartThingsConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add number entities for a config entry."""
    await number.async_setup_entry(hass, entry, async_add_entities)
