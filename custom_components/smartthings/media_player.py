"""Support for media players through the SmartThings cloud API."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import media_player

from . import SmartThingsConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add media players for a config entry."""
    await media_player.async_setup_entry(hass, entry, async_add_entities)
