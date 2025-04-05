"""Support for button entities through the SmartThings cloud API."""

from __future__ import annotations

from dataclasses import dataclass

from pysmartthings import Capability, Command, SmartThings

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity

from homeassistant.components.smartthings import button


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add button entities for a config entry."""
    await button.async_setup_entry(hass, entry, async_add_entities)
