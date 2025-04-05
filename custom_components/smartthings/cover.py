"""Support for covers through the SmartThings cloud API."""

from __future__ import annotations

from typing import Any

from pysmartthings import Attribute, Capability, Command, SmartThings

from homeassistant.components.cover import (
    ATTR_POSITION,
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
    CoverState,
)
from homeassistant.const import ATTR_BATTERY_LEVEL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, cover
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity

VALUE_TO_STATE = {
    "closed": CoverState.CLOSED,
    "closing": CoverState.CLOSING,
    "open": CoverState.OPEN,
    "opening": CoverState.OPENING,
    "partially open": CoverState.OPEN,
    "unknown": None,
}

CAPABILITIES = (Capability.WINDOW_SHADE, Capability.DOOR_CONTROL)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add covers for a config entry."""
    await cover.async_setup_entry(hass, entry, async_add_entities)
