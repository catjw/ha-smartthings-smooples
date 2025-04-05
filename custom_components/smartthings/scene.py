"""Support for scenes through the SmartThings cloud API."""

from typing import Any

from pysmartthings import Scene as STScene, SmartThings

from homeassistant.components.scene import Scene
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import SmartThingsConfigEntry, scene


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add lights for a config entry."""
    await scene.async_setup_entry(hass, entry, async_add_entities)
