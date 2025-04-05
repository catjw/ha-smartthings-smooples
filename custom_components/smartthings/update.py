"""Support for update entities through the SmartThings cloud API."""

from __future__ import annotations

from typing import Any

from awesomeversion import AwesomeVersion
from pysmartthings import Attribute, Capability, Command

from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import SmartThingsConfigEntry, update
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add update entities for a config entry."""
    await update.async_setup_entry(hass, entry, async_add_entities)
    